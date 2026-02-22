import os
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

for dir_path in [DATA_DIR, DATA_DIR / "raw", DATA_DIR / "processed", DATA_DIR / "exports", LOGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

CITIES_ANTIOQUIA = [
    "Medellín",
    "Envigado",
    "Sabaneta",
    "Itagüí",
    "Bello",
    "Rionegro",
    "La Estrella",
    "Caldas",
    "Copacabana",
    "Girardota",
    "Barbosa",
    "Antioquia",
]

SMMLV_2024 = 1423500

PLATFORMS = {
    "linkedin": {
        "name": "LinkedIn",
        "base_url": "https://co.linkedin.com/jobs",
        "search_url": "https://co.linkedin.com/jobs/search/?keywords={keyword}&location=Antioquia%2C%20Colombia",
        "requires_login": True,
    },
    "computrabajo": {
        "name": "Computrabajo",
        "base_url": "https://www.computrabajo.com.co",
        "search_url": "https://www.computrabajo.com.co/empleos-en-antioquia.html",
        "requires_login": False,
    },
    "indeed": {
        "name": "Indeed",
        "base_url": "https://co.indeed.com",
        "search_url": "https://co.indeed.com/jobs?q=&l=Antioquia%2C+Antioquia",
        "requires_login": False,
    },
    "magneto365": {
        "name": "Magneto365",
        "base_url": "https://www.magneto365.com",
        "search_url": "https://www.magneto365.com/co/empleos-en-antioquia",
        "requires_login": False,
    },
    "elempleo": {
        "name": "Elempleo",
        "base_url": "https://www.elempleo.com",
        "search_url": "https://www.elempleo.com/co/empleos/antioquia",
        "requires_login": False,
    },
    "masempleo": {
        "name": "MasEmpleo",
        "base_url": "https://www.masempleo.com.co",
        "search_url": "https://www.masempleo.com.co/empleos-en-antioquia",
        "requires_login": False,
    },
}

SECTOR_CATEGORIES = [
    "Tecnología",
    "Finanzas",
    "Manufactura",
    "Servicios",
    "Salud",
    "Educación",
    "Comercio",
    "Construcción",
    "Agricultura",
    "Transporte",
    "Turismo",
    "Telecomunicaciones",
    "Alimentos",
    "Automotriz",
    "Químico",
    "Textil",
    "Otro",
]

CARGO_NIVELES = [
    "Junior",
    "Semi-senior",
    "Senior",
    "Gerente",
    "Director",
    "VP",
    "C-Level",
    "Analista",
    "Asistente",
    "Coordinador",
    "Supervisor",
    "Jefe",
    "Vicepresidente",
]

CARGO_AREAS = [
    "IT",
    "Marketing",
    "Ventas",
    "Operaciones",
    "RRHH",
    "Finanzas",
    "Contabilidad",
    "Legal",
    "Ingeniería",
    "Producción",
    "Calidad",
    "Compras",
    "Logística",
    "Cartera",
    "Atención al Cliente",
    "Administrativo",
    "Otro",
]

MODALIDADES = ["Presencial", "Remoto", "Híbrido"]

TIPOS_CONTRATO = ["Indefinido", "Término fijo", "Prestacion de servicios", "Obra labor", "Temporal"]

JORNADAS = ["Tiempo completo", "Medio tiempo", "Freelance", "Por horas"]

EDUCACION_NIVELES = ["Bachillerato", "Técnico", "Tecnólogo", "Pregrado", "Posgrado", "Doctorado"]

HEADERS = {
    "User-Agent": "DataCollector Antioquia - Scraper Educational - Contacto: researcher@local",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "es-CO,es;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

REQUEST_TIMEOUT = 30
RATE_LIMIT_DELAY = 1.0
MAX_RETRIES = 3
RETRY_BACKOFF = 2

LOG_FILE = LOGS_DIR / f"scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
