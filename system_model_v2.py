"""
System Model V2 - With Citation Tracking (Phase 3)
Extends the original System class to track paper sources
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class System:
    """
    Represents a system with mechanisms and citation information
    """
    name: str
    domain: str
    type: List[str]  # e.g., ["field"], ["network"], ["population"]
    mechanisms: List[str]  # e.g., ["diffusion", "feedback"]

    # NEW: Citation tracking fields
    paper_title: Optional[str] = None
    authors: Optional[str] = None
    year: Optional[int] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    abstract: Optional[str] = None

    # Metadata
    added_by: str = "system"  # "system", "user", "paper_extraction", "arxiv"
    added_date: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON storage"""
        return {
            "name": self.name,
            "domain": self.domain,
            "type": self.type,
            "mechanisms": self.mechanisms,
            "paper_title": self.paper_title,
            "authors": self.authors,
            "year": self.year,
            "doi": self.doi,
            "url": self.url,
            "abstract": self.abstract,
            "added_by": self.added_by,
            "added_date": self.added_date
        }

    @staticmethod
    def from_dict(data: Dict) -> 'System':
        """Create System from dictionary"""
        return System(
            name=data.get("name", "Unknown"),
            domain=data.get("domain", "unknown"),
            type=data.get("type", []),
            mechanisms=data.get("mechanisms", []),
            paper_title=data.get("paper_title"),
            authors=data.get("authors"),
            year=data.get("year"),
            doi=data.get("doi"),
            url=data.get("url"),
            abstract=data.get("abstract"),
            added_by=data.get("added_by", "system"),
            added_date=data.get("added_date")
        )

    def has_citation(self) -> bool:
        """Check if system has citation information"""
        return self.paper_title is not None or self.authors is not None

    def get_citation_string(self) -> str:
        """Get formatted citation string"""
        if not self.has_citation():
            return "No citation available"

        parts = []

        if self.paper_title:
            parts.append(f'"{self.paper_title}"')

        if self.authors:
            parts.append(self.authors)

        if self.year:
            parts.append(f"({self.year})")

        citation = " ".join(parts)

        if self.doi:
            citation += f" DOI: {self.doi}"

        return citation

    def __repr__(self):
        citation = f" [{self.get_citation_string()}]" if self.has_citation() else ""
        return f"System({self.name}, {self.domain}, {self.mechanisms}{citation})"


# Backward compatibility: create simple System without citations
def System_simple(name: str, domain: str, type: List[str], mechanisms: List[str], 
                  constraints: Optional[List[str]] = None) -> System:
    """
    Backward compatible System creation (for existing code)
    """
    return System(
        name=name,
        domain=domain,
        type=type,
        mechanisms=mechanisms,
        added_by="system"
    )
