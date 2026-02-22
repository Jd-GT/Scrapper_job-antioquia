from datetime import datetime, timedelta
from typing import Dict, List, Tuple

from config import settings


class JobValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate(self, job: dict) -> Tuple[bool, List[str], List[str]]:
        self.errors = []
        self.warnings = []
        
        self._validate_company(job)
        self._validate_cargo(job)
        self._validate_location(job)
        self._validate_dates(job)
        self._validate_salary(job)
        self._validate_url(job)
        
        is_valid = len(self.errors) == 0
        
        return is_valid, self.errors, self.warnings
    
    def _validate_company(self, job: dict):
        empresa_nombre = job.get("empresa_nombre", "")
        
        if not empresa_nombre:
            self.errors.append("empresa_nombre está vacío")
        elif len(empresa_nombre) < 2:
            self.errors.append(f"empresa_nombre demasiado corto: {empresa_nombre}")
        
        if empresa_nombre and empresa_nombre.lower() in ["confidencial", "confidential", "anonimo"]:
            self.warnings.append("Empresa confidencial - verificar manualmente")
    
    def _validate_cargo(self, job: dict):
        cargo_titulo = job.get("cargo_titulo", "")
        
        if not cargo_titulo:
            self.errors.append("cargo_titulo está vacío")
        elif len(cargo_titulo) < 5:
            self.errors.append(f"cargo_titulo demasiado corto: {cargo_titulo}")
    
    def _validate_location(self, job: dict):
        location = job.get("empresa_ubicacion_exacta", "")
        
        if not location:
            self.errors.append("empresa_ubicacion_exacta está vacío")
            return
        
        is_valid_location = False
        for city in settings.CITIES_ANTIOQUIA:
            if city.lower() in location.lower():
                is_valid_location = True
                break
        
        if not is_valid_location:
            self.errors.append(f"Ubicación no es de Antioquia: {location}")
    
    def _validate_dates(self, job: dict):
        fecha_publicacion = job.get("fecha_publicacion", "")
        fecha_scraping = job.get("fecha_scraping", "")
        
        if not fecha_publicacion:
            self.errors.append("fecha_publicacion está vacío")
            return
        
        try:
            pub_date = datetime.strptime(fecha_publicacion, "%Y-%m-%d")
            today = datetime.now()
            
            if pub_date > today:
                self.errors.append(f"fecha_publicacion es futura: {fecha_publicacion}")
            
            max_days = timedelta(days=90)
            if today - pub_date > max_days:
                self.warnings.append(f"fecha_publicacion > 90 días: {fecha_publicacion}")
        
        except ValueError:
            self.errors.append(f"fecha_publicacion formato inválido: {fecha_publicacion}")
        
        if fecha_scraping:
            try:
                scrap_date = datetime.strptime(fecha_scraping, "%Y-%m-%d")
                today = datetime.now()
                if scrap_date > today:
                    self.errors.append(f"fecha_scraping es futura: {fecha_scraping}")
            except ValueError:
                self.warnings.append(f"fecha_scraping formato inválido: {fecha_scraping}")
    
    def _validate_salary(self, job: dict):
        salario_min = job.get("salario_min")
        salario_max = job.get("salario_max")
        
        if salario_min is not None and salario_max is not None:
            if salario_min > salario_max:
                self.errors.append(f"salario_min ({salario_min}) > salario_max ({salario_max})")
            
            if salario_min < settings.SMMLV_2024 * 0.5:
                self.warnings.append(f"salario_min suspiciously bajo: {salario_min}")
            
            if salario_max > settings.SMMLV_2024 * 100:
                self.warnings.append(f"salario_max suspiciously alto: {salario_max}")
    
    def _validate_url(self, job: dict):
        url = job.get("url_oferta", "")
        
        if not url:
            self.errors.append("url_oferta está vacío")
            return
        
        if not url.startswith("http"):
            self.errors.append(f"url_oferta no es URL válida: {url}")
        
        if not any(platform in url.lower() for platform in ["linkedin", "computrabajo", "indeed", "magneto", "elempleo", "masempleo"]):
            self.warnings.append(f"url_oferta no contiene plataforma conocida: {url}")
    
    def validate_batch(self, jobs: list) -> Tuple[list, list, list]:
        valid_jobs = []
        invalid_jobs = []
        validation_results = []
        
        for job in jobs:
            is_valid, errors, warnings = self.validate(job)
            result = {
                "job": job,
                "is_valid": is_valid,
                "errors": errors,
                "warnings": warnings
            }
            validation_results.append(result)
            
            if is_valid:
                valid_jobs.append(job)
            else:
                invalid_jobs.append(job)
        
        return valid_jobs, invalid_jobs, validation_results


def filter_antioquia_jobs(jobs: list) -> list:
    filtered = []
    for job in jobs:
        location = job.get("empresa_ubicacion_exacta", "")
        if location:
            for city in settings.CITIES_ANTIOQUIA:
                if city.lower() in location.lower():
                    filtered.append(job)
                    break
    return filtered


def deduplicate_jobs(jobs: list) -> list:
    seen = set()
    unique_jobs = []
    
    for job in jobs:
        url = job.get("url_oferta", "")
        job_id = job.get("id_oferta_plataforma", "")
        plataforma = job.get("plataforma_origen", "")
        
        key = (plataforma, job_id) if job_id else url
        
        if key and key not in seen:
            seen.add(key)
            unique_jobs.append(job)
        elif not key:
            unique_jobs.append(job)
    
    return unique_jobs
