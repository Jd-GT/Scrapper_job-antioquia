import re
from typing import Optional, Tuple

from config import settings


def parse_salary(salary_text: str) -> Tuple[Optional[float], Optional[float], Optional[str]]:
    if not salary_text:
        return None, None, None
    
    salary_text = salary_text.upper().replace(",", "").replace(" ", "")
    
    monthly_match = re.search(r'\$?([\d.]+)\s*[KM]?\s*-\s*\$?([\d.]+)\s*[KM]?', salary_text)
    if monthly_match:
        min_val = _convert_to_number(monthly_match.group(1), salary_text)
        max_val = _convert_to_number(monthly_match.group(2), salary_text)
        return min_val, max_val, "Mensual"
    
    single_match = re.search(r'\$?([\d.]+)\s*[KM]?', salary_text)
    if single_match:
        val = _convert_to_number(single_match.group(1), salary_text)
        return val, val, "Mensual"
    
    smmlv_match = re.search(r'(\d+)\s*SMMLV', salary_text)
    if smmlv_match:
        smmlv_count = int(smmlv_match.group(1))
        val = smmlv_count * settings.SMMLV_2024
        return val, val, "Mensual"
    
    return None, None, None


def _convert_to_number(value: str, context: str) -> float:
    num = float(value)
    if "K" in context:
        num *= 1000
    elif "M" in context:
        num *= 1000000
    return num


def parse_experience(text: str) -> Optional[int]:
    if not text:
        return None
    
    text_lower = text.lower()
    
    years_match = re.search(r'(\d+)\s*(?:año|year)', text_lower)
    if years_match:
        return int(years_match.group(1))
    
    range_match = re.search(r'(\d+)\s*-\s*(\d+)\s*(?:año|year)', text_lower)
    if range_match:
        return int(range_match.group(1))
    
    if "sin experiencia" in text_lower or "sin experiencia" in text_lower:
        return 0
    
    if "1 año" in text_lower or "un año" in text_lower:
        return 1
    
    if "2 años" in text_lower or "dos años" in text_lower:
        return 2
    
    return None


def parse_education(text: str) -> str:
    if not text:
        return ""
    
    text_lower = text.lower()
    
    if "doctorado" in text_lower or "phd" in text_lower:
        return "Doctorado"
    elif "posgrado" in text_lower or "maestría" in text_lower or "maestria" in text_lower or "master" in text_lower:
        return "Posgrado"
    elif "pregrado" in text_lower or "universidad" in text_lower or "licenciatura" in text_lower:
        return "Pregrado"
    elif "tecnólogo" in text_lower or "tecnologo" in text_lower:
        return "Tecnólogo"
    elif "técnico" in text_lower or "tecnico" in text_lower:
        return "Técnico"
    elif "bachillerato" in text_lower or "bachiller" in text_lower:
        return "Bachillerato"
    
    return ""


def extract_skills(text: str) -> Tuple[list, list]:
    if not text:
        return [], []
    
    text_lower = text.lower()
    
    tech_skills = [
        "python", "java", "javascript", "typescript", "c#", "c++", "c ", "ruby", "go", "rust",
        "php", "swift", "kotlin", "scala", "r ", "matlab", "sql", "mongodb", "postgresql", 
        "mysql", "oracle", "redis", "elasticsearch", "aws", "azure", "gcp", "docker", 
        "kubernetes", "jenkins", "git", "linux", "windows", "macos", "react", "angular", 
        "vue", "django", "flask", "spring", "node", "express", "nextjs", "nuxt", "flutter",
        "react native", "ionic", "machine learning", "deep learning", "tensorflow", "pytorch",
        "pandas", "numpy", "scikit", "tableau", "power bi", "excel", "spark", "hadoop",
        "hive", "kafka", "rest api", "graphql", "microservices", "agile", "scrum"
    ]
    
    soft_skills = [
        "comunicación", "comunicacion", "liderazgo", "trabajo en equipo", "equipo",
        "proactivo", "proactiva", "analítico", "analitica", "resolución de problemas",
        "adaptable", "flexible", "creativo", "organizado", "responsable", "puntual",
        "comprometido", "iniciativa", "autodidacta", "gestión del tiempo", "negociación",
        "atención al cliente", "servicio al cliente", "orientado a resultados"
    ]
    
    found_tech = [skill for skill in tech_skills if skill in text_lower]
    found_soft = [skill for skill in soft_skills if skill in text_lower]
    
    return list(set(found_tech)), list(set(found_soft))


def normalize_company_name(name: str) -> str:
    if not name:
        return "Confidencial"
    
    name = name.strip()
    
    common_names = {
        "bancolombia s.a.": "Bancolombia",
        "bancolombia sa": "Bancolombia",
        "ecopetrol s.a.": "Ecopetrol",
        "ecopetrol sa": "Ecopetrol",
        "sura": "Suramericana",
        "grupo sura": "Suramericana",
        "Grupo Nutresa": "Grupo Nutresa",
        "Grupo Éxito": "Grupo Éxito",
        "alkosto": "Alkosto",
        "falabella": "Falabella",
        "homecenter": "Homecenter",
        "credisura": "Credisura",
    }
    
    name_lower = name.lower()
    for key, value in common_names.items():
        if key in name_lower:
            return value
    
    return name


def normalize_sector(sector: str) -> str:
    if not sector:
        return ""
    
    sector_lower = sector.lower()
    
    sector_mapping = {
        "tecnología": "Tecnología",
        "tecnologia": "Tecnología",
        "ti": "Tecnología",
        "it": "Tecnología",
        "software": "Tecnología",
        "informática": "Tecnología",
        "informatica": "Tecnología",
        "finanzas": "Finanzas",
        "bancos": "Finanzas",
        "banca": "Finanzas",
        "aseguradora": "Finanzas",
        "manufactura": "Manufactura",
        "manufacturing": "Manufactura",
        "industrial": "Manufactura",
        "producción": "Manufactura",
        "servicios": "Servicios",
        "salud": "Salud",
        "médico": "Salud",
        "medico": "Salud",
        "hospital": "Salud",
        "educación": "Educación",
        "educacion": "Educación",
        "universidad": "Educación",
        "comercio": "Comercio",
        "retail": "Comercio",
        "construcción": "Construcción",
        "construccion": "Construcción",
        "agricultura": "Agricultura",
        "agro": "Agricultura",
        "transporte": "Transporte",
        "logística": "Logística",
        "logistica": "Logística",
        "turismo": "Turismo",
        "hotelería": "Hotelería",
        "hoteleria": "Hotelería",
        "telecom": "Telecomunicaciones",
        "telecomunicaciones": "Telecomunicaciones",
        "alimentos": "Alimentos",
        "alimentacion": "Alimentos",
        "automotriz": "Automotriz",
        "automovil": "Automotriz",
        "química": "Químico",
        "quimica": "Químico",
        "textil": "Textil",
        "confección": "Textil",
        "confeccion": "Textil",
    }
    
    for key, value in sector_mapping.items():
        if key in sector_lower:
            return value
    
    return sector


def normalize_location(location: str) -> str:
    if not location:
        return ""
    
    location_lower = location.lower()
    
    for city in settings.CITIES_ANTIOQUIA:
        if city.lower() in location_lower:
            return city
    
    return location
