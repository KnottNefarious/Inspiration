import json
import os
from system_model import System

DATABASE_FILE = "data/learned_systems.json"


def default_systems():

    return [

# -----------------------------
# Physics
# -----------------------------

System("Fluid Dynamics","physics",["field"],["diffusion","feedback","chaos"],[]),
System("Heat Diffusion","physics",["field"],["diffusion"],[]),
System("Wave Equation","physics",["field"],["oscillation","propagation"],[]),
System("Quantum Wavefunction","physics",["field"],["oscillation","interference"],[]),
System("Gravitational N-body","physics",["particles"],["attraction","feedback"],[]),
System("Magnetic Field Dynamics","physics",["field"],["feedback","propagation"],[]),
System("Plasma Dynamics","physics",["field"],["diffusion","feedback"],[]),
System("Turbulent Flow","physics",["field"],["chaos","diffusion"],[]),
System("Laser Oscillation","physics",["field"],["oscillation","feedback"],[]),
System("Electromagnetic Field","physics",["field"],["propagation","oscillation"],[]),

# -----------------------------
# Biology
# -----------------------------

System("Population Growth","biology",["population"],["competition","adaptation"],[]),
System("Predator Prey","biology",["population"],["competition","feedback","oscillation"],[]),
System("Gene Regulation Network","biology",["network"],["feedback","adaptation"],[]),
System("Neural Activity","biology",["network"],["adaptation","feedback","diffusion"],[]),
System("Immune Response","biology",["network"],["adaptation","selection","feedback"],[]),
System("Ecosystem Dynamics","biology",["population"],["competition","feedback"],[]),
System("Bacterial Colony Growth","biology",["population"],["diffusion","competition"],[]),
System("Cell Signaling","biology",["network"],["propagation","feedback"],[]),
System("Protein Interaction Network","biology",["network"],["interaction","feedback"],[]),
System("Evolutionary Dynamics","biology",["population"],["selection","mutation"],[]),

# -----------------------------
# Neuroscience
# -----------------------------

System("Neural Network","neuroscience",["graph"],["adaptation","optimization","feedback"],[]),
System("Synaptic Plasticity","neuroscience",["network"],["adaptation","feedback"],[]),
System("Brain Oscillations","neuroscience",["network"],["oscillation","feedback"],[]),
System("Cortical Wave Propagation","neuroscience",["field"],["diffusion","propagation"],[]),
System("Decision Networks","neuroscience",["network"],["competition","feedback"],[]),

# -----------------------------
# Computer Science
# -----------------------------

System("Distributed Systems","computer science",["network"],["coordination","feedback"],[]),
System("PageRank","computer science",["graph"],["diffusion","optimization"],[]),
System("Genetic Algorithm","computer science",["population"],["selection","mutation","optimization"],[]),
System("Reinforcement Learning","computer science",["agent"],["adaptation","optimization","feedback"],[]),
System("Swarm Optimization","computer science",["agents"],["adaptation","diffusion"],[]),
System("Ant Colony Optimization","computer science",["agents"],["diffusion","optimization"],[]),
System("Consensus Algorithm","computer science",["network"],["coordination","feedback"],[]),
System("Graph Neural Network","computer science",["graph"],["diffusion","adaptation"],[]),
System("Monte Carlo Search","computer science",["agents"],["exploration","selection"],[]),
System("Game AI Dynamics","computer science",["agents"],["competition","optimization"],[]),

# -----------------------------
# Economics
# -----------------------------

System("Market Economy","economics",["agents"],["competition","adaptation","optimization"],[]),
System("Supply Demand Model","economics",["agents"],["feedback","competition"],[]),
System("Financial Market Dynamics","economics",["agents"],["competition","feedback","chaos"],[]),
System("Innovation Diffusion","economics",["network"],["diffusion","adaptation"],[]),
System("Auction Dynamics","economics",["agents"],["competition","optimization"],[]),
System("Game Theory Dynamics","economics",["agents"],["competition","selection"],[]),
System("Economic Growth","economics",["population"],["adaptation","feedback"],[]),

# -----------------------------
# Social Systems
# -----------------------------

System("Rumor Spread","social",["network"],["diffusion"],[]),
System("Opinion Dynamics","social",["network"],["competition","adaptation"],[]),
System("Social Influence","social",["network"],["propagation","feedback"],[]),
System("Cultural Evolution","social",["population"],["selection","adaptation"],[]),
System("Information Cascades","social",["network"],["diffusion","feedback"],[]),
System("Collective Behavior","social",["agents"],["coordination","feedback"],[]),

# -----------------------------
# Engineering
# -----------------------------

System("Traffic Network","engineering",["network"],["congestion","diffusion","feedback"],[]),
System("Power Grid","engineering",["network"],["coordination","feedback"],[]),
System("Control Systems","engineering",["feedback loop"],["feedback","optimization"],[]),
System("Internet Routing","engineering",["network"],["optimization","diffusion"],[]),
System("Sensor Networks","engineering",["network"],["coordination","propagation"],[]),
System("Robotics Swarms","engineering",["agents"],["coordination","adaptation"],[]),

# -----------------------------
# Chemistry
# -----------------------------

System("Chemical Reaction","chemistry",["particles"],["reaction","feedback"],[]),
System("Reaction Diffusion","chemistry",["field"],["diffusion","reaction"],[]),
System("Oscillating Reaction","chemistry",["particles"],["oscillation","feedback"],[]),
System("Catalytic Networks","chemistry",["network"],["reaction","feedback"],[]),

# -----------------------------
# Ecology
# -----------------------------

System("Food Web","ecology",["network"],["competition","feedback"],[]),
System("Species Migration","ecology",["population"],["diffusion","adaptation"],[]),
System("Forest Dynamics","ecology",["population"],["competition","adaptation"],[]),

# -----------------------------
# Epidemiology
# -----------------------------

System("Disease Spread","epidemiology",["population"],["diffusion","infection"],[]),
System("Epidemic Models","epidemiology",["population"],["diffusion","feedback"],[]),

# -----------------------------
# Additional cross-domain models
# -----------------------------

System("Lotka Volterra Dynamics","math",["population"],["competition","oscillation"],[]),
System("Replicator Dynamics","math",["population"],["selection","competition"],[]),
System("Gradient Flow","math",["field"],["optimization"],[]),
System("Diffusion Equation","math",["field"],["diffusion"],[]),
System("Kuramoto Oscillators","math",["network"],["oscillation","coordination"],[])

    ]


def load_systems():

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


def save_systems(systems):

    with open(DATABASE_FILE,"w") as f:
        json.dump([s.to_dict() for s in systems],f,indent=2)