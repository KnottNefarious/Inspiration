"""
Paper System Extractor - Phase 3
Extracts system information from research papers
"""

import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from system_model_v2 import System


# ========================================
# MECHANISM KEYWORDS
# ========================================

MECHANISM_KEYWORDS = {
    "diffusion": [
        "diffusion", "spread", "propagation", "permeation", "transmission",
        "diffuse", "spreading", "contagion", "viral"
    ],
    "optimization": [
        "optimization", "optimize", "maximization", "minimization",
        "gradient descent", "optimal", "improve", "enhance"
    ],
    "competition": [
        "competition", "competitive", "rivalry", "contest",
        "zero-sum", "resource competition", "competitive advantage"
    ],
    "feedback": [
        "feedback", "feedback loop", "negative feedback", "positive feedback",
        "homeostasis", "regulation", "control loop"
    ],
    "selection": [
        "selection", "natural selection", "evolutionary selection",
        "survival", "fitness", "selective pressure"
    ],
    "adaptation": [
        "adaptation", "adaptive", "learning", "plasticity",
        "adjust", "evolve", "self-organizing"
    ],
    "oscillation": [
        "oscillation", "periodic", "rhythmic", "cyclic",
        "oscillate", "wave", "vibration"
    ],
    "coordination": [
        "coordination", "synchronization", "consensus",
        "swarm", "collective", "distributed coordination"
    ],
    "chaos": [
        "chaos", "chaotic", "strange attractor", "butterfly effect",
        "sensitive dependence", "nonlinear dynamics"
    ],
    "reaction": [
        "reaction", "chemical reaction", "catalysis",
        "reaction-diffusion", "autocatalytic"
    ]
}


# ========================================
# DOMAIN KEYWORDS
# ========================================

DOMAIN_KEYWORDS = {
    "biology": ["biological", "organism", "cell", "gene", "protein", "evolution", "ecology"],
    "physics": ["physical", "quantum", "particle", "field", "wave", "energy"],
    "computer science": ["algorithm", "computational", "network", "neural", "machine learning", "AI"],
    "neuroscience": ["neural", "brain", "neuron", "synaptic", "cognitive"],
    "chemistry": ["chemical", "molecule", "catalyst", "reaction"],
    "mathematics": ["mathematical", "theorem", "proof", "equation"],
    "economics": ["economic", "market", "trade", "financial"],
    "social": ["social", "society", "cultural", "human"],
    "engineering": ["engineering", "system design", "control"],
    "ecology": ["ecological", "ecosystem", "species", "population"]
}


# ========================================
# PAPER EXTRACTOR
# ========================================

class PaperExtractor:
    """
    Extracts system information from research papers
    """

    def __init__(self):
        pass


    def extract_from_text(self, text: str, paper_metadata: Optional[Dict] = None) -> List[System]:
        """
        Extract systems from paper text

        Args:
            text: Full text of paper (or abstract)
            paper_metadata: Dict with title, authors, year, doi, url

        Returns:
            List of System objects
        """

        if paper_metadata is None:
            paper_metadata = {}

        systems = []

        # Extract system names (heuristic: look for capitalized multi-word phrases)
        system_names = self._extract_system_names(text)

        # For each potential system name
        for name in system_names:
            # Extract mechanisms mentioned near this system
            mechanisms = self._extract_mechanisms_for_system(text, name)

            # Detect domain
            domain = self._detect_domain(text)

            # Determine type (simplified)
            sys_type = self._infer_type(text, name)

            if mechanisms:  # Only add if we found at least one mechanism
                system = System(
                    name=name,
                    domain=domain,
                    type=sys_type,
                    mechanisms=mechanisms,
                    paper_title=paper_metadata.get('title'),
                    authors=paper_metadata.get('authors'),
                    year=paper_metadata.get('year'),
                    doi=paper_metadata.get('doi'),
                    url=paper_metadata.get('url'),
                    abstract=text[:500] if len(text) > 500 else text,
                    added_by="paper_extraction",
                    added_date=datetime.now().isoformat()
                )

                systems.append(system)

        return systems


    def _extract_system_names(self, text: str) -> List[str]:
        """
        Extract potential system names from text
        Uses heuristics: capitalized phrases, common patterns
        """

        # Pattern 1: "X System", "X Model", "X Dynamics", "X Network"
        pattern1 = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(System|Model|Dynamics|Network|Process|Mechanism)\b'
        matches1 = re.findall(pattern1, text)
        names = [f"{m[0]} {m[1]}" for m in matches1]

        # Pattern 2: Common system types with adjectives
        pattern2 = r'\b(Neural|Genetic|Evolutionary|Swarm|Cellular|Agent|Multi-agent|Complex)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b'
        matches2 = re.findall(pattern2, text)
        names.extend([f"{m[0]} {m[1]}" for m in matches2])

        # Pattern 3: Title of paper often contains system name
        # (First sentence or first 100 chars)
        first_line = text.split('\n')[0][:100]
        if len(first_line) > 10:
            names.append(first_line.strip())

        # Remove duplicates and very long names
        names = list(set(names))
        names = [n for n in names if len(n) < 80 and len(n) > 5]

        return names[:5]  # Limit to top 5


    def _extract_mechanisms_for_system(self, text: str, system_name: str) -> List[str]:
        """
        Extract mechanisms mentioned in context of system
        """

        text_lower = text.lower()
        detected_mechanisms = []

        for mechanism, keywords in MECHANISM_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    detected_mechanisms.append(mechanism)
                    break  # Found this mechanism, move to next

        return list(set(detected_mechanisms))  # Remove duplicates


    def _detect_domain(self, text: str) -> str:
        """
        Detect the domain/field of the paper
        """

        text_lower = text.lower()
        domain_scores = {}

        for domain, keywords in DOMAIN_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                domain_scores[domain] = score

        if domain_scores:
            # Return domain with highest score
            return max(domain_scores.items(), key=lambda x: x[1])[0]

        return "unknown"


    def _infer_type(self, text: str, system_name: str) -> List[str]:
        """
        Infer system type (network, field, population, etc.)
        """

        text_lower = text.lower()
        name_lower = system_name.lower()

        types = []

        if any(word in text_lower or word in name_lower for word in ["network", "graph", "node", "edge"]):
            types.append("network")

        if any(word in text_lower or word in name_lower for word in ["field", "spatial", "continuum"]):
            types.append("field")

        if any(word in text_lower or word in name_lower for word in ["population", "agent", "individual"]):
            types.append("population")

        if any(word in text_lower or word in name_lower for word in ["particle", "point"]):
            types.append("particles")

        if not types:
            types = ["system"]  # Default

        return types


    def extract_from_abstract(self, abstract: str, paper_metadata: Optional[Dict] = None) -> List[System]:
        """
        Simplified extraction from just abstract (faster, less accurate)
        """
        return self.extract_from_text(abstract, paper_metadata)


# ========================================
# CONVENIENCE FUNCTIONS
# ========================================

def extract_systems_from_paper(text: str, title: Optional[str] = None, authors: Optional[str] = None,
                               year: Optional[int] = None, doi: Optional[str] = None, url: Optional[str] = None) -> List[System]:
    """
    Convenience function to extract systems from a paper

    Args:
        text: Paper text or abstract
        title: Paper title
        authors: Authors string
        year: Publication year
        doi: DOI
        url: URL

    Returns:
        List of System objects
    """

    metadata = {
        'title': title,
        'authors': authors,
        'year': year,
        'doi': doi,
        'url': url
    }

    extractor = PaperExtractor()
    return extractor.extract_from_text(text, metadata)


# ========================================
# TESTING
# ========================================

if __name__ == "__main__":

    print("="*70)
    print("PAPER EXTRACTOR - TEST")
    print("="*70)

    # Test with sample abstract
    sample_abstract = """
    Neural Cellular Automata: Learning to Grow Complex Patterns

    We present a method for training neural networks to grow complex 
    patterns through local interactions. The system uses a simple 
    cellular automaton updated by a learned neural network. Through 
    self-organization and adaptation, the system can regenerate 
    patterns even after damage. We demonstrate coordination between 
    cells and emergent feedback loops that maintain homeostasis.
    The model exhibits oscillatory behavior and chaotic dynamics
    under certain parameters.
    """

    metadata = {
        'title': 'Neural Cellular Automata',
        'authors': 'Mordvintsev et al.',
        'year': 2020,
        'doi': '10.23915/distill.00023',
        'url': 'https://distill.pub/2020/growing-ca/'
    }

    extractor = PaperExtractor()
    systems = extractor.extract_from_text(sample_abstract, metadata)

    print(f"\nExtracted {len(systems)} system(s):\n")

    for i, sys in enumerate(systems, 1):
        print(f"System {i}:")
        print(f"  Name: {sys.name}")
        print(f"  Domain: {sys.domain}")
        print(f"  Type: {sys.type}")
        print(f"  Mechanisms: {sys.mechanisms}")
        print(f"  Citation: {sys.get_citation_string()}")
        print()

    print("="*70)
    print("Test complete!")
    print("="*70)
