import argparse
import logging
import sys
from datetime import datetime

from config import settings
from scrapers.computrabajo import ComputrabajoScraper
from scrapers.elempleo import ElempleoScraper
from scrapers.indeed import IndeedScraper
from scrapers.linkedin import LinkedInScraper
from scrapers.magneto365 import Magneto365Scraper
from scrapers.masempleo import MasEmpleoScraper
from scrapers.computrabajo_selenium import ComputrabajoSeleniumScraper
from scrapers.indeed_selenium import IndeedSeleniumScraper
from scrapers.elempleo_selenium import ElempleoSeleniumScraper
from utils.exporter import DataExporter
from utils.parser import parse_salary
from utils.validator import JobValidator, deduplicate_jobs


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("main")


SCRAPERS = {
    "linkedin": LinkedInScraper,
    "computrabajo": ComputrabajoScraper,
    "indeed": IndeedScraper,
    "magneto365": Magneto365Scraper,
    "elempleo": ElempleoScraper,
    "masempleo": MasEmpleoScraper,
}

SCRAPERS_SELENIUM = {
    "linkedin": LinkedInScraper,
    "computrabajo": ComputrabajoSeleniumScraper,
    "indeed": IndeedSeleniumScraper,
    "magneto365": Magneto365Scraper,
    "elempleo": ElempleoSeleniumScraper,
    "masempleo": MasEmpleoScraper,
}

IT_KEYWORDS = [
    "desarrollador",
    "ingeniero de software",
    "programador",
    "analista",
    "soporte técnico",
    "desarrollador python",
    "desarrollador java",
]


def normalize_job(job: dict) -> dict:
    if job.get("salario_texto_original"):
        min_sal, max_sal, tipo = parse_salary(job["salario_texto_original"])
        job["salario_min"] = min_sal
        job["salario_max"] = max_sal
        job["salario_tipo"] = tipo or "Mensual"
    
    return job


def run_scraper(platform: str, max_pages: int = 5, keyword: str = None, use_selenium: bool = False, headless: bool = True) -> list:
    scrapers_map = SCRAPERS_SELENIUM if use_selenium else SCRAPERS
    
    if platform not in scrapers_map:
        logger.error(f"Plataforma desconocida: {platform}")
        return []
    
    if not keyword:
        keyword = IT_KEYWORDS[0]
        logger.info(f"Usando keyword de IT por defecto: {keyword}")
    
    logger.info(f"Iniciando scraper para {platform} {'(Selenium)' if use_selenium else ''}")
    
    scraper_class = scrapers_map[platform]
    scraper = scraper_class(headless=headless) if use_selenium and hasattr(scraper_class, '__init__') else scraper_class()
    
    try:
        jobs = scraper.scrape(keyword=keyword, max_pages=max_pages)
        
        if hasattr(scraper, 'close'):
            scraper.close()
        
        normalized_jobs = [normalize_job(job) for job in jobs]
        
        logger.info(f"{platform}: {len(normalized_jobs)} empleos encontrados")
        return normalized_jobs
        
    except Exception as e:
        logger.error(f"Error en {platform}: {e}")
        if hasattr(scraper, 'close'):
            try:
                scraper.close()
            except:
                pass
        return []


def main():
    parser = argparse.ArgumentParser(description="Data Collector - Empleos Antioquia")
    parser.add_argument("--platforms", nargs="+", default=list(SCRAPERS.keys()),
                       help="Plataformas a scrapear")
    parser.add_argument("--max-pages", type=int, default=5,
                       help="Máximo de páginas por plataforma")
    parser.add_argument("--keyword", type=str, default=None,
                       help="Palabra clave para buscar")
    parser.add_argument("--validate", action="store_true",
                       help="Validar empleos después de scrape")
    parser.add_argument("--export", action="store_true", default=True,
                       help="Exportar datos")
    parser.add_argument("--use-selenium", action="store_true",
                       help="Usar Selenium (navegador real) para evitar bloqueos")
    parser.add_argument("--headless", action="store_true", default=True,
                       help="Ejecutar Selenium sin interfaz (default: True)")
    parser.add_argument("--debug", action="store_true",
                       help="Abrir navegador visible para depurar selectores")
    
    args = parser.parse_args()
    
    logger.info("="*60)
    logger.info("Data Collector - Empleos Antioquia")
    logger.info("="*60)
    logger.info(f"Plataformas: {args.platforms}")
    logger.info(f"Máx páginas: {args.max_pages}")
    logger.info(f"Palabra clave: {args.keyword or IT_KEYWORDS[0]} (IT por defecto)")
    logger.info(f"Modo Selenium: {args.use_selenium}")
    logger.info(f"Modo debug: {args.debug} (navegador visible)")
    logger.info("="*60)
    
    all_jobs = []
    
    headless_mode = not args.debug
    
    for platform in args.platforms:
        jobs = run_scraper(platform, args.max_pages, args.keyword, args.use_selenium, headless=headless_mode)
        all_jobs.extend(jobs)
    
    logger.info(f"\nTotal empleos recolectados: {len(all_jobs)}")
    
    all_jobs = deduplicate_jobs(all_jobs)
    logger.info(f"Después de deduplicar: {len(all_jobs)}")
    
    if args.validate:
        logger.info("\nValidando empleos...")
        validator = JobValidator()
        valid_jobs, invalid_jobs, results = validator.validate_batch(all_jobs)
        
        logger.info(f"Válidos: {len(valid_jobs)}")
        logger.info(f"Inválidos: {len(invalid_jobs)}")
        
        for result in results:
            if not result["is_valid"]:
                logger.warning(f"Job inválido: {result['errors']}")
        
        all_jobs = valid_jobs
    
    if args.export and all_jobs:
        logger.info("\nExportando datos...")
        exporter = DataExporter()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        exporter.export_all_formats(all_jobs, f"empleos_antioquia_{timestamp}")
        
        exporter.print_summary(all_jobs)
    
    logger.info("\n✓ Proceso completado")


if __name__ == "__main__":
    main()
