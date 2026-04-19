from bs4 import BeautifulSoup
import httpx
import click
import colorama
import tqdm
import os
import re
import ssl
import socket
import json
import time
import banner
import concurrent.futures

# Read the .env mannually 
if os.path.exists('.env'):
    with open('.env') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, _, value = line.partition('=')
                os.environ.setdefault(key.strip(), value.strip())


SHODAN_KEY   = os.getenv('SHODAN_API_KEY')   
URLSCAN_KEY  = os.getenv('URLSCAN_API_KEY')   

# 
class Spidy:
    def __init__(self, target, shodan_key=None, urlscan_key=None):
        self.target      = target        
        self.shodan_key  = shodan_key    
        self.urlscan_key = urlscan_key   
        self.results     = {}  

    def get_subdomains(self):
        # Extract domain from target (remove www if present)
        domain = self.target.replace('www.', '')

        # Query crt.sh for subdomains via certificate transparency
        try:
            crt_url = f'https://crt.sh/?q=%25.{domain}&output=json'
            crt_response = httpx.get(crt_url, timeout=10)
            crt_data = crt_response.json()
            
            subdomains = set()
            for entry in crt_data:
                name_value = entry.get('name_value', '')
                for subdomain in name_value.split('\n'):
                    subdomain = subdomain.strip()
                    if subdomain and subdomain.endswith(domain):
                        subdomains.add(subdomain)
            
            # Extract SAN from TLS certificate
            try:
                context = ssl.create_default_context()
                with socket.create_connection((domain, 443), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=domain) as ssock:
                        cert = ssock.getpeercert()
                        san_list = cert.get('subjectAltName', [])
                        for san_type, san_value in san_list:
                            if san_type == 'DNS':
                                subdomains.add(san_value)
            except Exception as e:
                pass
            
            self.results['subdomains'] = sorted(list(subdomains))
            return self.results['subdomains']
        except Exception as e:
            return []

    def lookup(self):
        try:
            subdomains = self.results.get('subdomains', [])
            if not subdomains:
                return
            
            lookup_results = {}
            for subdomain in tqdm.tqdm(subdomains, desc="Looking up subdomains"):
                try:
                    url = f'https://{subdomain}'
                    response = httpx.get(url, timeout=10, follow_redirects=True)
                    
                    if response.status_code in [200, 301, 403]:
                        lookup_results[subdomain] = {
                            'status_code': response.status_code,
                            'headers': dict(response.headers),
                            'cookies': dict(response.cookies),
                            'stack': response.text[:500]
                        }
                except Exception as e:
                    lookup_results[subdomain] = {'error': str(e)}
            
            self.results['lookup'] = lookup_results
            return lookup_results
        except Exception as e:
            return {}
    
    def crawl(self):
        try:
            subdomains = self.results.get('subdomains', [])
            if not subdomains:
                return []
            
            crawl_results = {}
            for subdomain in tqdm.tqdm(subdomains, desc="Crawling subdomains"):
                try:
                    base_url = f'https://{subdomain}'
                    crawl_results[subdomain] = {
                        'endpoints': [],
                        'js_files': [],
                        'robots': None,
                        'sitemap': None,
                        'security_headers': {}
                    }
                    
                    # Main page
                    response = httpx.get(base_url, timeout=10, follow_redirects=True)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extract endpoints and JS files
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        if href.startswith('/') or href.startswith(base_url):
                            crawl_results[subdomain]['endpoints'].append(href)
                    
                    for script in soup.find_all('script', src=True):
                        src = script['src']
                        if src.startswith('/') or src.startswith(base_url):
                            crawl_results[subdomain]['js_files'].append(src)
                    
                    # Security headers
                    crawl_results[subdomain]['security_headers'] = dict(response.headers)
                    
                    # robots.txt
                    try:
                        robots_resp = httpx.get(f'{base_url}/robots.txt', timeout=5)
                        if robots_resp.status_code == 200:
                            crawl_results[subdomain]['robots'] = robots_resp.text
                    except:
                        pass
                    
                    # sitemap.xml
                    try:
                        sitemap_resp = httpx.get(f'{base_url}/sitemap.xml', timeout=5)
                        if sitemap_resp.status_code == 200:
                            crawl_results[subdomain]['sitemap'] = sitemap_resp.text
                    except:
                        pass
                        
                except Exception as e:
                    crawl_results[subdomain] = {'error': str(e)}
            
            self.results['crawl'] = crawl_results
            return crawl_results
        except Exception as e:
            return {}

    def shodan(self):
        if not self.shodan_key:
            return {}

        try:
            subdomains = self.results.get('subdomains', [])
            if not subdomains:
                return {}
            
            shodan_results = {}
            for subdomain in tqdm.tqdm(subdomains, desc="Querying Shodan"):
                try:
                    # Resolve subdomain to IP
                    try:
                        ip = socket.gethostbyname(subdomain)
                    except socket.gaierror:
                        continue
                    
                    # Query Shodan API for IP
                    shodan_url = f'https://api.shodan.io/shodan/host/{ip}'
                    params = {'key': self.shodan_key}
                    response = httpx.get(shodan_url, params=params, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        shodan_results[subdomain] = {
                            'ip': ip,
                            'ports': data.get('ports', []),
                            'services': [
                                {
                                    'port': port,
                                    'service': service.get('name', 'unknown'),
                                    'product': service.get('product', '')
                                }
                                for port, service in zip(data.get('ports', []), data.get('data', []))
                            ],
                            'organization': data.get('org', ''),
                            'os': data.get('os', '')
                        }
                except Exception as e:
                    pass
            
            self.results['shodan'] = shodan_results
            return shodan_results
        except Exception as e:
            return {}

    def wbm(self):
        try:
            crawl_data = self.results.get('crawl', {})
            if not crawl_data:
                return []
            
            params_results = []
            for subdomain, data in crawl_data.items():
                endpoints = data.get('endpoints', [])
                
                for endpoint in tqdm.tqdm(endpoints, desc=f"Analyzing params for {subdomain}"):
                    try:
                        url = endpoint if endpoint.startswith('http') else f'https://{subdomain}{endpoint}'
                        response = httpx.get(url, timeout=10, follow_redirects=True)
                        
                        # Extract query parameters from URL
                        if '?' in url:
                            query_string = url.split('?')[1]
                            params = [p.split('=')[0] for p in query_string.split('&')]
                            params_results.append({
                                'subdomain': subdomain,
                                'endpoint': endpoint,
                                'parameters': params,
                                'status_code': response.status_code
                            })
                    except Exception as e:
                        pass
            
            self.results['parameters'] = params_results
            return params_results
        except Exception as e:
            return []

    def usio(self):
        if not self.urlscan_key:
            return {}

        try:
            subdomains = self.results.get('subdomains', [])
            if not subdomains:
                return {}
            
            urlscan_results = {}
            for subdomain in tqdm.tqdm(subdomains, desc="Querying URLScan"):
                try:
                    url = f'https://{subdomain}'
                    
                    # Submit scan to URLScan
                    submit_url = 'https://urlscan.io/api/v1/scan/'
                    headers = {'API-Key': self.urlscan_key}
                    payload = {'url': url, 'visibility': 'public'}
                    
                    response = httpx.post(submit_url, json=payload, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        scan_data = response.json()
                        scan_uuid = scan_data.get('uuid')
                        
                        # Wait and retrieve results
                        time.sleep(5)
                        
                        result_url = f'https://urlscan.io/api/v1/result/{scan_uuid}/'
                        result_response = httpx.get(result_url, headers=headers, timeout=10)
                        
                        if result_response.status_code == 200:
                            result_data = result_response.json()
                            urlscan_results[subdomain] = {
                                'screenshot': result_data.get('screenshot'),
                                'technologies': result_data.get('meta', {}).get('technologies', []),
                                'requests': result_data.get('data', {}).get('requests', []),
                                'cookies': result_data.get('data', {}).get('cookies', []),
                                'page': result_data.get('page', {}),
                                'scan_id': scan_uuid
                            }
                except Exception as e:
                    pass
            
            self.results['urlscan'] = urlscan_results
            return urlscan_results
        except Exception as e:
            return {}

def main():
    def _save_report(results, output, target, out_format):
        os.makedirs(output, exist_ok=True)
        report_file = os.path.join(output, f'{target.replace(".", "_")}.{out_format}')

        if out_format == 'json':
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
        else:
            html_content = f"""<html>
<head><meta charset="utf-8"><title>nn0nn report</title></head>
<body>
<pre>{json.dumps(results, indent=2, ensure_ascii=False)}</pre>
</body>
</html>"""
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

        return report_file

    @click.command(context_settings={"help_option_names": ["-h", "--help"]})
    @click.option('-t', '--target', required=True, help='Target domain to analyze')
    @click.option('-o', '--output', default='./output/', show_default=True, help='Output directory')
    @click.option('--shodan/--no-shodan', default=False, help='Enable Shodan correlation')
    @click.option('--urlscan/--no-urlscan', default=False, help='Enable URLScan compilation')
    @click.option('-v', '--verbose', is_flag=True, help='Verbose output')
    @click.option('--format', 'out_format', type=click.Choice(['json', 'html']), default='json', show_default=True, help='Report format')
    def cli(target, output, shodan, urlscan, verbose, out_format):
        banner.banner()

        if verbose:
            banner.info('Verbose mode enabled')

        banner.info(f'Target: {target}')
        if shodan and not SHODAN_KEY:
            banner.warn('Shodan flag enabled but SHODAN_API_KEY is not set')
        if urlscan and not URLSCAN_KEY:
            banner.warn('URLScan flag enabled but URLSCAN_API_KEY is not set')

        spider = Spidy(
            target,
            shodan_key=SHODAN_KEY if shodan else None,
            urlscan_key=URLSCAN_KEY if urlscan else None
        )

        banner.info('Enumerating subdomains')
        subdomains = spider.get_subdomains()
        banner.ok(f'Found {len(subdomains)} subdomains')

        banner.info('Looking up subdomains')
        spider.lookup()

        banner.info('Crawling discovered subdomains')
        spider.crawl()

        if shodan:
            banner.info('Querying Shodan')
            spider.shodan()

        banner.info('Extracting parameters from crawled endpoints')
        spider.wbm()

        if urlscan:
            banner.info('Querying URLScan')
            spider.usio()

        try:
            report_path = _save_report(spider.results, output, target, out_format)
            banner.ok(f'Report saved to {report_path}')
        except Exception as exc:
            banner.error(f'Unable to write report: {exc}')

    cli()

if __name__ == '__main__':
    main()