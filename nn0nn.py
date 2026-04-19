import bs4 
import httpx 
import lxml, jinja2, shodan
import click
import colorama, tqdm, pyfiglet
import os, sys

# Leer el .env manualmente y cargar cada línea como variable de entorno
if os.path.exists('.env'):
    with open('.env') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, _, value = line.partition('=')
                os.environ.setdefault(key.strip(), value.strip())

# Ahora ya puedes leerlas
SHODAN_KEY   = os.getenv('SHODAN_API_KEY')    # None si no está
URLSCAN_KEY  = os.getenv('URLSCAN_API_KEY')   # None si no está
