import httpx

# Creating the client
class HTTPClient:
    def __init__(self, config):
        self.client = httpx.Client(
            timeout=config.timeout,
            follow_redirects=config.follow_redirects,
            headers={'User-Agent': config.user_agent}
        )

    def get(self, url):
        return self.client.get(url)
    
    def close(self):
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

