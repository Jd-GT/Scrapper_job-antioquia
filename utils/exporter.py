import json
from datetime import datetime
from pathlib import Path
from typing import List

import pandas as pd

from config import settings


class DataExporter:
    def __init__(self):
        self.data_dir = settings.DATA_DIR
    
    def to_jsonl(self, jobs: List[dict], filename: str) -> Path:
        filepath = self.data_dir / "raw" / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for job in jobs:
                f.write(json.dumps(job, ensure_ascii=False) + '\n')
        
        print(f"✓ JSONL: {filepath} ({len(jobs)} jobs)")
        return filepath
    
    def to_jsonl_processed(self, jobs: List[dict], filename: str) -> Path:
        filepath = self.data_dir / "processed" / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for job in jobs:
                f.write(json.dumps(job, ensure_ascii=False) + '\n')
        
        print(f"✓ JSONL processed: {filepath} ({len(jobs)} jobs)")
        return filepath
    
    def to_csv(self, jobs: List[dict], filename: str) -> Path:
        filepath = self.data_dir / "exports" / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        df = pd.DataFrame(jobs)
        df.to_csv(filepath, index=False, encoding='utf-8')
        
        print(f"✓ CSV: {filepath} ({len(jobs)} jobs)")
        return filepath
    
    def to_parquet(self, jobs: List[dict], filename: str) -> Path:
        filepath = self.data_dir / "exports" / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        df = pd.DataFrame(jobs)
        df.to_parquet(filepath, index=False)
        
        print(f"✓ Parquet: {filepath} ({len(jobs)} jobs)")
        return filepath
    
    def export_all_formats(self, jobs: List[dict], base_filename: str):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = f"{base_filename}_{timestamp}"
        
        self.to_jsonl(jobs, f"{name}.jsonl")
        self.to_jsonl_processed(jobs, f"{name}_processed.jsonl")
        self.to_csv(jobs, f"{name}.csv")
        
        if len(jobs) > 100:
            self.to_parquet(jobs, f"{name}.parquet")
        
        return name
    
    def load_jsonl(self, filepath: str) -> List[dict]:
        jobs = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    jobs.append(json.loads(line))
        return jobs
    
    def get_summary(self, jobs: List[dict]) -> dict:
        if not jobs:
            return {"total": 0}
        
        df = pd.DataFrame(jobs)
        
        summary = {
            "total": len(jobs),
            "por_plataforma": df['plataforma_origen'].value_counts().to_dict() if 'plataforma_origen' in df else {},
            "por_ciudad": df['empresa_ubicacion_exacta'].value_counts().to_dict() if 'empresa_ubicacion_exacta' in df else {},
            "con_salario": len(df[df['salario_min'].notna()]) if 'salario_min' in df else 0,
            "remotos": len(df[df['cargo_modalidad'] == 'Remoto']) if 'cargo_modalidad' in df else 0,
            "presenciales": len(df[df['cargo_modalidad'] == 'Presencial']) if 'cargo_modalidad' in df else 0,
            "hibridos": len(df[df['cargo_modalidad'] == 'Híbrido']) if 'cargo_modalidad' in df else 0,
        }
        
        if 'salario_min' in df:
            salary_data = df[df['salario_min'].notna()]['salario_min']
            if not salary_data.empty:
                summary["salario_min_promedio"] = float(salary_data.mean())
                summary["salario_min_mediana"] = float(salary_data.median())
        
        return summary
    
    def print_summary(self, jobs: List[dict]):
        summary = self.get_summary(jobs)
        
        print("\n" + "="*50)
        print("RESUMEN DE DATOS")
        print("="*50)
        print(f"Total de ofertas: {summary['total']}")
        
        if summary.get('por_plataforma'):
            print("\nPor plataforma:")
            for platform, count in summary['por_plataforma'].items():
                print(f"  - {platform}: {count}")
        
        if summary.get('por_ciudad'):
            print("\nPor ciudad (top 10):")
            for city, count in list(summary['por_ciudad'].items())[:10]:
                print(f"  - {city}: {count}")
        
        print(f"\nOfertas con salario: {summary.get('con_salario', 0)}")
        print(f"Remotos: {summary.get('remotos', 0)}")
        print(f"Presenciales: {summary.get('presenciales', 0)}")
        print(f"Híbridos: {summary.get('hibridos', 0)}")
        
        if summary.get('salario_min_promedio'):
            print(f"\nSalario mínimo promedio: ${summary['salario_min_promedio']:,.0f} COP")
            print(f"Salario mínimo mediana: ${summary['salario_min_mediana']:,.0f} COP")
        
        print("="*50)
