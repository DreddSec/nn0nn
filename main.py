import click
from config import load_config
from client import HTTPClient
import banner


@click.command()
@click.option('--target', '-t', required=True, help='IP address target')
@click.option('--output', '-o', default='./output', help='Name of the report')
@click.option('--format', '-f', default='json', help='The report format')
@click.option('--shodan', is_flag=True, help='Optional scan with shodan')
def cli(target, output, format, shodan):
    banner.banner()
    config = load_config()

    with HTTPClient(config) as client:
        banner.info(f'Starting recon on {target}')
        pass

if __name__ == '__main__':
    cli()
