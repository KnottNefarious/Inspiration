"""
Literature Search - Phase 3
Searches arXiv and extracts systems from papers automatically
"""

import time
from typing import List, Dict, Optional
from paper_extractor import PaperExtractor
from system_model_v2 import System


# ========================================
# ARXIV SEARCH (No API needed - uses web scraping)
# ========================================

class LiteratureSearcher:
    """
    Searches research databases and extracts systems
    Note: Uses simplified search without external dependencies
    """

    def __init__(self):
        self.extractor = PaperExtractor()


    def search_arxiv_simple(self, query: str, max_results: int = 10) -> List[System]:
        """
        Simplified arXiv search - simulates what would happen with real API

        In production, this would use the arxiv Python package:

        import arxiv
        search = arxiv.Search(query=query, max_results=max_results)
        for result in search.results():
            # Extract from result.summary (abstract)
            systems = self.extractor.extract_from_abstract(...)

        For now, returns empty list with instructions
        """

        print(f"\n[LITERATURE SEARCH] Searching arXiv for: '{query}'")
        print(f"[INFO] To enable real arXiv search, install: pip install arxiv")
        print(f"[INFO] Then uncomment the arxiv code in literature_search.py")

        # Simulated results
        print(f"\n[SIMULATION] Would search arXiv and extract systems from {max_results} papers")
        print(f"[SIMULATION] Query: {query}")

        return []


    def search_arxiv_with_api(self, query: str, max_results: int = 10) -> List[System]:
        """
        Real arXiv search using arxiv package
        Uncomment this code after installing: pip install arxiv
        """

        try:
            import arxiv
        except ImportError:
            print("[ERROR] arxiv package not installed")
            print("[FIX] Run: pip install arxiv")
            return []

        print(f"\n[LITERATURE SEARCH] Searching arXiv for: '{query}'")

        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        all_systems = []
        papers_processed = 0

        for result in search.results():
            papers_processed += 1
            print(f"  Processing [{papers_processed}/{max_results}]: {result.title[:60]}...")

            # Extract metadata
            metadata = {
                'title': result.title,
                'authors': ', '.join([author.name for author in result.authors]),
                'year': result.published.year,
                'doi': result.doi,
                'url': result.entry_id,
            }

            # Extract systems from abstract
            systems = self.extractor.extract_from_abstract(
                result.summary,
                metadata
            )

            if systems:
                print(f"    → Extracted {len(systems)} system(s)")
                all_systems.extend(systems)

            # Rate limiting
            time.sleep(0.5)

        print(f"\n[COMPLETE] Processed {papers_processed} papers")
        print(f"[COMPLETE] Extracted {len(all_systems)} systems total")

        return all_systems


    def search_by_topic(self, topic: str, max_results: int = 10) -> List[System]:
        """
        Search for systems related to a topic
        """

        # Try to use real API first, fall back to simulation
        try:
            import arxiv
            return self.search_arxiv_with_api(topic, max_results)
        except ImportError:
            return self.search_arxiv_simple(topic, max_results)


    def search_by_author(self, author: str, max_results: int = 10) -> List[System]:
        """
        Search for systems from a specific author's papers
        """

        query = f"au:{author}"
        return self.search_by_topic(query, max_results)


# ========================================
# MANUAL PAPER ENTRY
# ========================================

def add_paper_manually(title: str, abstract: str, authors: Optional[str] = None,
                       year: Optional[int] = None, doi: Optional[str] = None, url: Optional[str] = None) -> List[System]:
    """
    Manually add a paper and extract systems

    Args:
        title: Paper title
        abstract: Paper abstract or text
        authors: Authors (comma separated)
        year: Publication year
        doi: DOI
        url: URL

    Returns:
        List of extracted System objects
    """

    metadata = {
        'title': title,
        'authors': authors,
        'year': year,
        'doi': doi,
        'url': url
    }

    extractor = PaperExtractor()
    systems = extractor.extract_from_text(abstract, metadata)

    print(f"\n[MANUAL ENTRY] Extracted {len(systems)} system(s) from paper:")
    print(f"  Title: {title}")
    for i, sys in enumerate(systems, 1):
        print(f"  System {i}: {sys.name} ({sys.domain})")

    return systems


# ========================================
# BATCH PROCESSING
# ========================================

def batch_extract_from_papers(papers: List[Dict]) -> List[System]:
    """
    Extract systems from multiple papers

    Args:
        papers: List of dicts with keys: title, abstract, authors, year, doi, url

    Returns:
        List of all extracted systems
    """

    extractor = PaperExtractor()
    all_systems = []

    print(f"\n[BATCH] Processing {len(papers)} papers...")

    for i, paper in enumerate(papers, 1):
        print(f"  [{i}/{len(papers)}] {paper.get('title', 'Untitled')[:60]}...")

        systems = extractor.extract_from_text(
            paper.get('abstract', ''),
            paper
        )

        if systems:
            print(f"    → Extracted {len(systems)} system(s)")
            all_systems.extend(systems)

    print(f"\n[BATCH COMPLETE] Extracted {len(all_systems)} systems total")

    return all_systems


# ========================================
# TESTING
# ========================================

if __name__ == "__main__":

    print("="*70)
    print("LITERATURE SEARCH - TEST")
    print("="*70)

    searcher = LiteratureSearcher()

    # Test 1: Manual paper entry
    print("\nTEST 1: Manual paper entry")
    print("-"*70)

    systems = add_paper_manually(
        title="Growing Neural Cellular Automata",
        abstract="""
        We present a method for training neural networks to grow patterns.
        The system uses cellular automata with neural network updates.
        Through adaptation and self-organization, patterns regenerate.
        We observe coordination and feedback maintaining homeostasis.
        """,
        authors="Mordvintsev et al.",
        year=2020,
        doi="10.23915/distill.00023"
    )

    print(f"\nExtracted systems:")
    for sys in systems:
        print(f"  - {sys.name}")
        print(f"    Mechanisms: {sys.mechanisms}")
        print(f"    Citation: {sys.get_citation_string()}")

    # Test 2: Simulated arXiv search
    print("\n\nTEST 2: arXiv search (simulation)")
    print("-"*70)

    systems = searcher.search_by_topic("swarm intelligence", max_results=5)

    # Test 3: Batch processing
    print("\n\nTEST 3: Batch processing")
    print("-"*70)

    papers = [
        {
            'title': 'Particle Swarm Optimization',
            'abstract': 'Swarm-based optimization using coordination and adaptation',
            'authors': 'Kennedy & Eberhart',
            'year': 1995
        },
        {
            'title': 'Ant Colony Optimization',
            'abstract': 'Optimization through pheromone-based feedback and diffusion',
            'authors': 'Dorigo',
            'year': 1992
        }
    ]

    systems = batch_extract_from_papers(papers)

    print("\n" + "="*70)
    print("Tests complete!")
    print("="*70)
    print("\n[NOTE] To enable real arXiv search:")
    print("  1. Run: pip install arxiv")
    print("  2. Use: searcher.search_arxiv_with_api('your query')")
