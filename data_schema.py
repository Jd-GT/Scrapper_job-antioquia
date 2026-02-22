"""Data schema for job postings."""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class JobPosting:
    """Represents a single job posting."""
    
    title: str
    company: str
    location: str
    salary_raw: str = ""
    url: str = ""
    source: str = ""
    date_posted: Optional[str] = None
    
    # Processed fields
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary_type: str = "Mensual"
    contract_type: str = "No especificado"
    benefits: list = field(default_factory=list)
    zone: str = ""
    relevance_score: float = 0.0
    description: str = ""
    
    def to_dict(self):
        """Convert to dictionary for JSON export."""
        return {
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "salary_raw": self.salary_raw,
            "salary_min": self.salary_min,
            "salary_max": self.salary_max,
            "salary_type": self.salary_type,
            "contract_type": self.contract_type,
            "benefits": self.benefits,
            "zone": self.zone,
            "relevance_score": self.relevance_score,
            "url": self.url,
            "source": self.source,
            "date_posted": self.date_posted,
            "description": self.description,
        }
