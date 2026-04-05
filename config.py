import os
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Config:
    # API keys — se cargan desde variables de entorno
    shodan_api_key: Optional[str]     = field(default_factory=lambda: os.getenv("SHODAN_API_KEY"))
    virustotal_api_key: Optional[str] = field(default_factory=lambda: os.getenv("VT_API_KEY"))
    urlscan_api_key: Optional[str]    = field(default_factory=lambda: os.getenv("URLSCAN_API_KEY"))

    # HTTP
    timeout: int         = 10
    max_retries: int     = 2
    user_agent: str      = "nn0nn/1.0 (passive-recon)"
    follow_redirects: bool = True

    # Crawl
    max_depth: int       = 2
    max_pages: int       = 50
    same_domain_only: bool = True

    # Output
    output_dir: str      = "./output"
    report_formats: list = field(default_factory=lambda: ["json", "html"])

    # Feature flags — si no hay key, el módulo se desactiva solo
    @property
    def shodan_enabled(self) -> bool:
        return self.shodan_api_key is not None

    @property
    def virustotal_enabled(self) -> bool:
        return self.virustotal_api_key is not None

    @property
    def urlscan_enabled(self) -> bool:
        return self.urlscan_api_key is not None


def load_config() -> Config:
    """Carga la config intentando leer un .env si existe."""
    env_file = ".env"
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    os.environ.setdefault(key.strip(), value.strip())
    return Config()
