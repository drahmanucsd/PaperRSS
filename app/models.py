from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Paper:
    title: str
    doi: str
    link: str
    abstract: str
    journal: str
    published_date: datetime
    summary: Optional[str] = None
    
    def __post_init__(self):
        # Ensure DOI is in the correct format
        if not self.doi.startswith('10.'):
            self.doi = f"10.{self.doi}" 