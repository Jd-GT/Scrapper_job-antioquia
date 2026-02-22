import json
import re
from pathlib import Path
from typing import List, Dict, Any

# Palabras clave IT - MAS flexible para capturar más ofertas
IT_KEYWORDS = [
    # Desarrollo
    "desarrollador", "desarrolladora", "developer", "programador", "programadora",
    "fullstack", "full stack", "frontend", "front-end", "backend", "back-end",
    "web", "mobile", "app", "aplicaciones", "software", "sistema",
    
    # Data & AI
    "data", "datos", "analista", "analisis", "analisis de datos", "big data", 
    "machine learning", "ml", "data scientist", "data engineer", "etl", "inteligencia artificial",
    
    # Infra & DevOps
    "devops", "cloud", "aws", "azure", "gcp", "google cloud", "kubernetes", "k8s",
    "docker", "terraform", "ci/cd", "jenkins", "infraestructura", "sysadmin", "infra",
    "soporte tecnico", "soporte técnico", "helpdesk", "tecnico", "técnico", "tecnologia", "tecnología",
    
    # QA
    "qa", "quality", "tester", "testing", "pruebas", "calidad",
    
    # Security
    "cybersecurity", "seguridad informatica", "seguridad información", "ciberseguridad",
    
    # Tech roles
    "ingeniero sistemas", "ingeniera sistemas", "ingeniero software", "ingeniera software",
    "analista sistemas", "analista de sistemas", "programador", "desarrollador",
    "python", "java", "javascript", "node", "react", "angular", "vue", "vuejs",
    "django", "flask", ".net", "php", "ruby", "go", "golang", "swift", "kotlin",
    "sql", "mongodb", "mysql", "postgres", "oracle", "dba", "base de datos",
    "sap", "erp", "crm", "salesforce",
    "redes", "network", "cisco", "ccna", "ccnp",
    "ux", "ui", "diseño digital", "producto", "product manager",
    "scrum", "agile", "metodologias ágiles",
]

# Palabras a excluir - SOLO las muy claramente NO IT
EXCLUDE_KEYWORDS = [
    "conductor", "chofer", "vigilante", "guardia", 
    "cocinero", "cocina", "mesero", "camarero",
    "vendedor", "vendedora", "ventas", "comercial",
    "call center", "telemarketing",
    "profesor", "docente", "maestro", "tutor",
    "enfermero", "enfermera", "médico", "medico",
    "contador", "abogado", "abogacía",
    "recursos humanos", "rrhh", "gestión humana", "talento humano",
    "arquitecto", "construccion", "construcción", "obra civil",
    "mecánico", "mecanico", "electricista", "plomero", "carpintero",
    "soldador", "operario de producción", "fabrica", "fábrica",
    "agricultor", "ganadero", "veterinario", "ambiental",
    "marketing digital", "diseñador gráfico", "comunicador",
    "asesor financiero", "asesor de seguros",
]


def is_it_job(title: str, company: str = "", description: str = "") -> bool:
    """Determina si un trabajo es de TI/IT basado en el título"""
    text = f"{title} {company} {description}".lower()
    
    # Excluir primero
    for exclude in EXCLUDE_KEYWORDS:
        if exclude.lower() in text:
            return False
    
    # Buscar palabras IT
    for keyword in IT_KEYWORDS:
        if keyword.lower() in text:
            return True
    
    return False


def extract_skills_from_title(title: str) -> List[str]:
    """Extrae skills del título del trabajo"""
    title_lower = title.lower()
    skills = []
    
    # Programming languages
    if "python" in title_lower:
        skills.extend(["Python", "Django", "Flask"])
    if "java" in title_lower:
        skills.extend(["Java", "Spring"])
    if "javascript" in title_lower or "js" in title_lower:
        skills.extend(["JavaScript", "Node.js"])
    if "typescript" in title_lower:
        skills.extend(["TypeScript"])
    if ".net" in title_lower or "c#" in title_lower:
        skills.extend([".NET", "C#"])
    if "php" in title_lower:
        skills.extend(["PHP", "Laravel"])
    if "ruby" in title_lower:
        skills.extend(["Ruby", "Rails"])
    if "go" in title_lower or "golang" in title_lower:
        skills.extend(["Go", "Golang"])
    if "swift" in title_lower:
        skills.extend(["Swift"])
    if "kotlin" in title_lower:
        skills.extend(["Kotlin"])
    
    # Frameworks & Libraries
    if "react" in title_lower:
        skills.extend(["React", "React Native"])
    if "angular" in title_lower:
        skills.extend(["Angular"])
    if "vue" in title_lower:
        skills.extend(["Vue.js"])
    if "django" in title_lower:
        skills.append("Django")
    if "flask" in title_lower:
        skills.append("Flask")
    if "spring" in title_lower:
        skills.append("Spring")
    if "node" in title_lower:
        skills.append("Node.js")
    
    # Data & ML
    if "data" in title_lower or "datos" in title_lower:
        skills.extend(["SQL", "Excel", "Power BI"])
    if "machine learning" in title_lower or "ml " in title_lower:
        skills.extend(["Machine Learning", "Python", "TensorFlow"])
    if "analytics" in title_lower:
        skills.extend(["Analytics", "Tableau"])
    if "etl" in title_lower:
        skills.append("ETL")
    
    # DevOps & Cloud
    if "devops" in title_lower:
        skills.extend(["Docker", "Kubernetes", "CI/CD"])
    if "cloud" in title_lower:
        skills.extend(["AWS", "Azure", "GCP"])
    if "aws" in title_lower:
        skills.append("AWS")
    if "azure" in title_lower:
        skills.append("Azure")
    if "gcp" in title_lower:
        skills.append("Google Cloud")
    if "docker" in title_lower:
        skills.append("Docker")
    if "kubernetes" in title_lower or "k8s" in title_lower:
        skills.extend(["Kubernetes", "K8s"])
    if "terraform" in title_lower:
        skills.append("Terraform")
    if "jenkins" in title_lower:
        skills.append("Jenkins")
    
    # Databases
    if "sql" in title_lower:
        skills.append("SQL")
    if "mysql" in title_lower:
        skills.append("MySQL")
    if "postgres" in title_lower or "postgresql" in title_lower:
        skills.append("PostgreSQL")
    if "mongo" in title_lower:
        skills.append("MongoDB")
    if "oracle" in title_lower:
        skills.append("Oracle")
    if "redis" in title_lower:
        skills.append("Redis")
    
    # QA & Testing
    if "qa" in title_lower or "testing" in title_lower or "tester" in title_lower:
        skills.extend(["QA", "Testing", "Selenium"])
    if "selenium" in title_lower:
        skills.append("Selenium")
    if "cypress" in title_lower:
        skills.append("Cypress")
    
    # Support & IT
    if "soporte" in title_lower:
        skills.extend(["Soporte técnico", "Windows", "Linux", "Helpdesk"])
    if "infraestructura" in title_lower or "infra" in title_lower:
        skills.extend(["Infraestructura", "Redes"])
    if "redes" in title_lower or "network" in title_lower:
        skills.extend(["Redes", "Cisco", "VPN"])
    if "security" in title_lower or "seguridad" in title_lower:
        skills.extend(["Ciberseguridad", "Security"])
    if "sysadmin" in title_lower:
        skills.extend(["SysAdmin", "Linux", "Windows Server"])
    
    # General IT
    if "software" in title_lower or "desarrollador" in title_lower or "programador" in title_lower:
        skills.append("Desarrollo de Software")
    if "web" in title_lower:
        skills.append("Desarrollo Web")
    if "mobile" in title_lower or "móvil" in title_lower:
        skills.append("Desarrollo Mobile")
    if "fullstack" in title_lower or "full stack" in title_lower:
        skills.extend(["Full Stack", "Frontend", "Backend"])
    if "frontend" in title_lower or "front-end" in title_lower:
        skills.extend(["Frontend", "CSS", "HTML"])
    if "backend" in title_lower or "back-end" in title_lower:
        skills.append("Backend")
    if "erp" in title_lower or "sap" in title_lower:
        skills.extend(["SAP", "ERP"])
    if "crm" in title_lower:
        skills.append("CRM")
    
    # General IT skills - add common skills based on context
    if any(x in title_lower for x in ["soporte", "support", "tecnico", "técnico"]):
        skills.extend(["Soporte técnico", "Windows", "Helpdesk"])
    if any(x in title_lower for x in ["analista", "analisis", "analysis"]):
        skills.extend(["Análisis de datos", "Excel", "Reporting"])
    if any(x in title_lower for x in ["mejora continua", "procesos", "procesos"]):
        skills.extend(["Mejora continua", "Procesos", "Lean"])
    if any(x in title_lower for x in ["mantenimiento", "refrigeracion", "refrigeración"]):
        skills.extend(["Mantenimiento", "Refrigeración"])
    if any(x in title_lower for x in ["seguridad electronica", "electrónica"]):
        skills.extend(["Electrónica", "CCTV", "Seguridad electrónica"])
    if any(x in title_lower for x in ["cobros", "cartera", "creditos"]):
        skills.extend(["Cobros", "Cartera", "Créditos"])
    if any(x in title_lower for x in ["servicios", "servicio", "general"]):
        skills.extend(["Atención al cliente", "Servicio"])
    if any(x in title_lower for x in ["montallantas", "vehículo", "vehiculo"]):
        skills.extend(["Montaje", "Vehículos"])
    if any(x in title_lower for x in ["punto de servicio", "pdv"]):
        skills.extend(["PDV", "Puntos de venta"])
    if any(x in title_lower for x in ["auxiliar", "asistente"]):
        skills.extend(["Auxiliar", "Asistencia"])
    
    # Remove duplicates while preserving order
    seen = set()
    unique_skills = []
    for skill in skills:
        if skill.lower() not in seen:
            seen.add(skill.lower())
            unique_skills.append(skill)
    
    # If still no skills, add a default based on the area
    if not unique_skills:
        area = "IT"
        if any(x in title_lower for x in ["data", "datos", "analista"]):
            area = "Ciencia de Datos"
        elif any(x in title_lower for x in ["devops", "cloud", "infra"]):
            area = "DevOps"
        elif any(x in title_lower for x in ["qa", "test"]):
            area = "QA"
        elif any(x in title_lower for x in ["security", "seguridad"]):
            area = "Seguridad"
        unique_skills = [area]
    
    return unique_skills[:6]  # Max 6 skills


def filter_it_jobs(jobs: List[Dict]) -> List[Dict]:
    """Filtra solo trabajos de IT"""
    return [job for job in jobs if is_it_job(job.get("title", ""), job.get("company", ""))]


def transform_job_to_frontend(job: Dict, index: int) -> Dict:
    """Transforma un trabajo scrapeado al formato del frontend"""
    title = job.get("title", "")
    company = job.get("company", "No especificada")
    location = job.get("location", "")
    salary_raw = job.get("salary_raw", "")
    
    # Detectar nivel
    nivel = "Senior"
    if any(x in title.lower() for x in ["junior", "jr", "trainee", "practicante", "sin experiencia"]):
        nivel = "Junior"
    elif any(x in title.lower() for x in ["semi", "mid", "1-3", "2-4"]):
        nivel = "Semi-senior"
    
    # Detectar área IT
    area = "IT"
    title_lower = title.lower()
    if any(x in title_lower for x in ["data", "datos", "analista", "analytics"]):
        area = "Ciencia de Datos"
    elif any(x in title_lower for x in ["devops", "cloud", "infra"]):
        area = "DevOps"
    elif any(x in title_lower for x in ["qa", "test", "pruebas"]):
        area = "QA"
    elif any(x in title_lower for x in ["security", "seguridad", "cyber"]):
        area = "Seguridad"
    elif any(x in title_lower for x in ["redes", "network", "sysadmin"]):
        area = "Redes"
    
    # Detectar modalidad
    modalidad = "Presencial"
    if any(x in title_lower for x in ["remoto", "remote", "desde casa", "home office"]):
        modalidad = "Remoto"
    elif any(x in title_lower for x in ["híbrido", "hibrido", "hybrid"]):
        modalidad = "Híbrido"
    
    # Extraer salario
    salary_min = job.get("salary_min")
    salary_max = job.get("salary_max")
    
    # Si company es "No especificada", usar la ubicación como fallback
    if not company or company == "No especificada" or company.strip() == "":
        # Extraer ciudad de la ubicación
        city = location.split(",")[0].strip() if location else "Medellín"
        company = f"Empresa en {city}"
    
    # Extraer experiencia del título
    experiencia = 0
    if any(x in title_lower for x in ["junior", "jr", "jr.", "trainee", "practicante", "sin experiencia"]):
        experiencia = 1
    elif any(x in title_lower for x in ["semi", "mid", "1-3", "2-4"]):
        experiencia = 2
    elif any(x in title_lower for x in ["senior", "sr", "sr.", "5 años", "5+", "5-"]):
        experiencia = 5
    elif any(x in title_lower for x in ["lead", "líder", "coordinador", "jefe"]):
        experiencia = 6
    
    # Extraer skills del título
    habilidades_tecnicas = extract_skills_from_title(title)
    
    return {
        "id": str(index + 1),
        "plataforma_origen": job.get("source", "Computrabajo"),
        "empresa": {
            "nombre": company,
            "sector": "Tecnología",
            "tamaño": "No especificado",
            "ubicacion": location.replace(", Antioquia", "").replace(",", "").strip() if location else "Medellín",
            "verificada": False
        },
        "cargo": {
            "titulo": title,
            "nivel": nivel,
            "area": area,
            "modalidad": modalidad,
            "tipo_contrato": job.get("contract_type", "No especificado"),
            "jornada": "Tiempo completo"
        },
        "compensacion": {
            "salario_min": salary_min,
            "salario_max": salary_max,
            "moneda": "COP",
            "beneficios": []
        },
        "requisitos": {
            "experiencia_anos": experiencia,
            "educacion_minima": "No especificada",
            "habilidades_tecnicas": habilidades_tecnicas,
            "habilidades_blandas": [],
            "idiomas": []
        },
        "metadata": {
            "fecha_publicacion": job.get("date_posted", "2026-02-22"),
            "fecha_scraping": "2026-02-22",
            "url": job.get("url", ""),
            "estado": "Activa"
        }
    }


def load_and_filter_scraped_data(json_path: str = None) -> List[Dict]:
    """Carga los datos scrapeados y los filtra para solo IT"""
    if json_path is None:
        # Usar el archivo más reciente
        files = list(Path(".").glob("empleos_antioquia_*.json"))
        if not files:
            print("No se encontraron archivos de datos")
            return []
        json_path = str(max(files, key=lambda p: p.stat().st_mtime))
    
    print(f"Cargando datos de: {json_path}")
    
    with open(json_path, "r", encoding="utf-8") as f:
        jobs = json.load(f)
    
    print(f"Total trabajos cargados: {len(jobs)}")
    
    # Filtrar solo IT
    it_jobs = filter_it_jobs(jobs)
    print(f"Trabajos IT encontrados: {len(it_jobs)}")
    
    # Transformar al formato del frontend
    frontend_jobs = [transform_job_to_frontend(job, i) for i, job in enumerate(it_jobs)]
    
    return frontend_jobs


if __name__ == "__main__":
    jobs = load_and_filter_scraped_data()
    print(f"\n=== Resumen ===")
    print(f"Total trabajos IT: {len(jobs)}")
    
    if jobs:
        # Guardar para el frontend
        output_path = "frontend/lib/real-data.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(jobs, f, ensure_ascii=False, indent=2)
        print(f"\nDatos guardados en: {output_path}")
        
        print(f"\nPrimeros 5 trabajos IT:")
        for job in jobs[:5]:
            print(f"  - {job['cargo']['titulo']} @ {job['empresa']['nombre']} ({job['cargo']['area']})")
