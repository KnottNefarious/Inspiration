"""
System Database V2 - With Citation Support (Phase 3)
Manages systems with paper citations
"""

import json
import os
from system_model_v2 import System
from typing import List, Optional


DATABASE_FILE = "data/learned_systems.json"


def default_systems() -> List[System]:
    """
    Default systems (original 134 + citation support)
    """

    # Keep all original systems but use new System class
    systems = [
        # Physics
        System("Fluid Dynamics","physics",["field"],["diffusion","feedback","chaos"]),
        System("Heat Diffusion","physics",["field"],["diffusion"]),
        System("Wave Equation","physics",["field"],["oscillation","propagation"]),
        System("Quantum Wavefunction","physics",["field"],["oscillation","interference"]),
        System("Gravitational N-body","physics",["particles"],["attraction","feedback"]),
        System("Magnetic Field Dynamics","physics",["field"],["feedback","propagation"]),
        System("Plasma Dynamics","physics",["field"],["diffusion","feedback"]),
        System("Turbulent Flow","physics",["field"],["chaos","diffusion"]),
        System("Laser Oscillation","physics",["field"],["oscillation","feedback"]),
        System("Electromagnetic Field","physics",["field"],["propagation","oscillation"]),

        # Biology
        System("Population Growth","biology",["population"],["competition","adaptation"]),
        System("Predator Prey","biology",["population"],["competition","feedback","oscillation"]),
        System("Gene Regulation Network","biology",["network"],["feedback","adaptation"]),
        System("Neural Activity","biology",["network"],["adaptation","feedback","diffusion"]),
        System("Immune Response","biology",["network"],["adaptation","selection","feedback"]),
        System("Ecosystem Dynamics","biology",["population"],["competition","feedback"]),
        System("Bacterial Colony Growth","biology",["population"],["diffusion","competition"]),
        System("Cell Signaling","biology",["network"],["propagation","feedback"]),
        System("Protein Interaction Network","biology",["network"],["interaction","feedback"]),
        System("Evolutionary Dynamics","biology",["population"],["selection","mutation"]),

        # Neuroscience
        System("Neural Network","neuroscience",["graph"],["adaptation","optimization","feedback"]),
        System("Synaptic Plasticity","neuroscience",["network"],["adaptation","feedback"]),
        System("Brain Oscillations","neuroscience",["network"],["oscillation","feedback"]),
        System("Cortical Wave Propagation","neuroscience",["field"],["diffusion","propagation"]),
        System("Decision Networks","neuroscience",["network"],["competition","feedback"]),

        # Computer Science
        System("Distributed Systems","computer science",["network"],["coordination","feedback"]),
        System("PageRank","computer science",["graph"],["diffusion","optimization"]),
        System("Genetic Algorithm","computer science",["population"],["selection","mutation","optimization"]),
        System("Reinforcement Learning","computer science",["agent"],["adaptation","optimization","feedback"]),
        System("Swarm Optimization","computer science",["agents"],["adaptation","diffusion"]),
        System("Ant Colony Optimization","computer science",["agents"],["diffusion","optimization"]),
        System("Consensus Algorithm","computer science",["network"],["coordination","feedback"]),
        System("Graph Neural Network","computer science",["graph"],["diffusion","adaptation"]),
        System("Monte Carlo Search","computer science",["agents"],["exploration","selection"]),
        System("Game AI Dynamics","computer science",["agents"],["competition","optimization"]),

        # Economics
        System("Market Economy","economics",["agents"],["competition","adaptation","optimization"]),
        System("Supply Demand Model","economics",["agents"],["feedback","competition"]),
        System("Financial Market Dynamics","economics",["agents"],["competition","feedback","chaos"]),
        System("Innovation Diffusion","economics",["network"],["diffusion","adaptation"]),
        System("Auction Dynamics","economics",["agents"],["competition","optimization"]),
        System("Game Theory Dynamics","economics",["agents"],["competition","selection"]),
        System("Economic Growth","economics",["population"],["adaptation","feedback"]),

        # Social Systems
        System("Rumor Spread","social",["network"],["diffusion"]),
        System("Opinion Dynamics","social",["network"],["competition","adaptation"]),
        System("Social Influence","social",["network"],["propagation","feedback"]),
        System("Cultural Evolution","social",["population"],["selection","adaptation"]),
        System("Information Cascades","social",["network"],["diffusion","feedback"]),
        System("Collective Behavior","social",["agents"],["coordination","feedback"]),

        # Engineering
        System("Traffic Network","engineering",["network"],["congestion","diffusion","feedback"]),
        System("Power Grid","engineering",["network"],["coordination","feedback"]),
        System("Control Systems","engineering",["feedback loop"],["feedback","optimization"]),
        System("Internet Routing","engineering",["network"],["optimization","diffusion"]),
        System("Sensor Networks","engineering",["network"],["coordination","propagation"]),
        System("Robotics Swarms","engineering",["agents"],["coordination","adaptation"]),

        # Chemistry
        System("Chemical Reaction","chemistry",["particles"],["reaction","feedback"]),
        System("Reaction Diffusion","chemistry",["field"],["diffusion","reaction"]),
        System("Oscillating Reaction","chemistry",["particles"],["oscillation","feedback"]),
        System("Catalytic Networks","chemistry",["network"],["reaction","feedback"]),

        # Ecology
        System("Food Web","ecology",["network"],["competition","feedback"]),
        System("Species Migration","ecology",["population"],["diffusion","adaptation"]),
        System("Forest Dynamics","ecology",["population"],["competition","adaptation"]),

        # Epidemiology
        System("Disease Spread","epidemiology",["population"],["diffusion","infection"]),
        System("Epidemic Models","epidemiology",["population"],["diffusion","feedback"]),

        # Math Models
        System("Lotka Volterra Dynamics","math",["population"],["competition","oscillation"]),
        System("Replicator Dynamics","math",["population"],["selection","competition"]),
        System("Gradient Flow","math",["field"],["optimization"]),
        System("Diffusion Equation","math",["field"],["diffusion"]),
        System("Kuramoto Oscillators","math",["network"],["oscillation","coordination"])
    ]

    return systems


def load_systems() -> List[System]:
    """Load systems from database"""

    if not os.path.exists(DATABASE_FILE):
        systems = default_systems()
        save_systems(systems)
        return systems

    try:
        with open(DATABASE_FILE) as f:
            data = json.load(f)

        systems = [System.from_dict(x) for x in data]

        if len(systems) == 0:
            systems = default_systems()
            save_systems(systems)

        return systems

    except:
        systems = default_systems()
        save_systems(systems)
        return systems


def save_systems(systems: List[System]):
    """Save systems to database"""

    # Create data directory if needed
    os.makedirs("data", exist_ok=True)

    with open(DATABASE_FILE, "w") as f:
        json.dump([s.to_dict() for s in systems], f, indent=2)


def add_system(system: System):
    """Add a single system to database"""

    systems = load_systems()
    systems.append(system)
    save_systems(systems)

    print(f"[DATABASE] Added system: {system.name}")


def add_systems_batch(new_systems: List[System]):
    """Add multiple systems to database"""

    systems = load_systems()

    # Avoid duplicates by name
    existing_names = {s.name.lower() for s in systems}
    added = 0

    for sys in new_systems:
        if sys.name.lower() not in existing_names:
            systems.append(sys)
            existing_names.add(sys.name.lower())
            added += 1

    save_systems(systems)

    print(f"[DATABASE] Added {added} new systems (skipped {len(new_systems) - added} duplicates)")
    print(f"[DATABASE] Total systems: {len(systems)}")


def search_systems(query: Optional[str] = None, domain: Optional[str] = None, 
                  mechanism: Optional[str] = None, has_citation: Optional[bool] = None) -> List[System]:
    """
    Search systems by criteria

    Args:
        query: Search in name (case-insensitive)
        domain: Filter by domain
        mechanism: Filter by mechanism
        has_citation: Filter by citation presence

    Returns:
        List of matching systems
    """

    systems = load_systems()
    results = systems

    if query:
        query_lower = query.lower()
        results = [s for s in results if query_lower in s.name.lower()]

    if domain:
        results = [s for s in results if s.domain == domain]

    if mechanism:
        results = [s for s in results if mechanism in s.mechanisms]

    if has_citation is not None:
        results = [s for s in results if s.has_citation() == has_citation]

    return results


# ========================================
# STATISTICS
# ========================================

def get_database_stats() -> dict:
    """Get statistics about the database"""

    systems = load_systems()

    stats = {
        'total_systems': len(systems),
        'with_citations': sum(1 for s in systems if s.has_citation()),
        'without_citations': sum(1 for s in systems if not s.has_citation()),
        'domains': {},
        'mechanisms': {},
        'sources': {}
    }

    # Count by domain
    for sys in systems:
        stats['domains'][sys.domain] = stats['domains'].get(sys.domain, 0) + 1

    # Count by mechanism
    for sys in systems:
        for mech in sys.mechanisms:
            stats['mechanisms'][mech] = stats['mechanisms'].get(mech, 0) + 1

    # Count by source (added_by)
    for sys in systems:
        source = sys.added_by
        stats['sources'][source] = stats['sources'].get(source, 0) + 1

    return stats
