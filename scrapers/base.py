import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import settings
from config.selectors import get_selectors


class BaseScraper(ABC):
    def __init__(self, platform_name: str, platform_key: str):
        self.platform_name = platform_name
        self.platform_key = platform_key
        self.selectors = get_selectors(platform_key)
        self.session = self._create_session()
        self.logger = self._setup_logger()
        self.jobs = []

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        retry_strategy = Retry(
            total=settings.MAX_RETRIES,
            backoff_factor=settings.RETRY_BACKOFF,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        session.headers.update(settings.HEADERS)
        return session

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(f"scraper.{self.platform_key}")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.FileHandler(settings.LOG_FILE, encoding='utf-8')
            handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            logger.addHandler(handler)
            console = logging.StreamHandler()
            console.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
            logger.addHandler(console)
        return logger

    def _make_request(self, url: str, max_retries: int = None) -> Optional[BeautifulSoup]:
        max_retries = max_retries or settings.MAX_RETRIES
        for attempt in range(max_retries):
            try:
                self.logger.info(f"Requesting: {url} (attempt {attempt + 1})")
                response = self.session.get(url, timeout=settings.REQUEST_TIMEOUT)
                response.raise_for_status()
                time.sleep(settings.RATE_LIMIT_DELAY)
                return BeautifulSoup(response.content, 'lxml')
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Request failed: {e}")
                if attempt < max_retries - 1:
                    wait_time = settings.RETRY_BACKOFF ** attempt
                    self.logger.info(f"Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                else:
                    self.logger.error(f"Failed to fetch {url} after {max_retries} attempts")
        return None

    def _safe_extract(self, element, selector: str, attribute: str = None) -> str:
        if element is None:
            return ""
        try:
            if attribute:
                return element.get(attribute, "").strip()
            found = element.select_one(selector)
            return found.get_text(strip=True) if found else ""
        except Exception:
            return ""

    def _is_antioquia(self, location: str) -> bool:
        if not location:
            return False
        location_lower = location.lower()
        return any(city.lower() in location_lower for city in settings.CITIES_ANTIOQUIA)

    def _create_job_object(self, data: dict) -> dict:
        return {
            "empresa_nombre": data.get("empresa_nombre", ""),
            "empresa_sector": data.get("empresa_sector", ""),
            "empresa_tamaño": data.get("empresa_tamaño", ""),
            "empresa_ubicacion_exacta": data.get("empresa_ubicacion_exacta", ""),
            "empresa_verificada": data.get("empresa_verificada", False),
            "cargo_titulo": data.get("cargo_titulo", ""),
            "cargo_nivel": data.get("cargo_nivel", ""),
            "cargo_area": data.get("cargo_area", ""),
            "cargo_modalidad": data.get("cargo_modalidad", ""),
            "cargo_tipo_contrato": data.get("cargo_tipo_contrato", ""),
            "cargo_jornada": data.get("cargo_jornada", ""),
            "salario_min": data.get("salario_min"),
            "salario_max": data.get("salario_max"),
            "salario_texto_original": data.get("salario_texto_original", ""),
            "salario_tipo": data.get("salario_tipo", "Mensual"),
            "beneficios": data.get("beneficios", []),
            "experiencia_requerida_anos": data.get("experiencia_requerida_anos"),
            "educacion_minima": data.get("educacion_minima", ""),
            "habilidades_tecnicas": data.get("habilidades_tecnicas", []),
            "habilidades_blandas": data.get("habilidades_blandas", []),
            "idiomas_requeridos": data.get("idiomas_requeridos", []),
            "plataforma_origen": self.platform_name,
            "fecha_publicacion": data.get("fecha_publicacion", ""),
            "fecha_scraping": datetime.now().strftime("%Y-%m-%d"),
            "url_oferta": data.get("url_oferta", ""),
            "id_oferta_plataforma": data.get("id_oferta_plataforma", ""),
            "estado_oferta": data.get("estado_oferta", "Activa"),
        }

    @abstractmethod
    def scrape(self, keyword: str = None, max_pages: int = 5) -> list:
        pass

    def scrape_job_details(self, url: str) -> dict:
        soup = self._make_request(url)
        if not soup:
            return {}
        return self._parse_job_details(soup)

    @abstractmethod
    def _parse_job_details(self, soup: BeautifulSoup) -> dict:
        pass

    def save_jobs(self, filepath: str = None):
        import json
        from pathlib import Path
        
        if not filepath:
            filepath = settings.DATA_DIR / "raw" / f"{self.platform_key}_jobs.jsonl"
        
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for job in self.jobs:
                f.write(json.dumps(job, ensure_ascii=False) + '\n')
        
        self.logger.info(f"Saved {len(self.jobs)} jobs to {filepath}")
