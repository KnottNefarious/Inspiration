import random
import requests
from sympy import symbols, Function, Eq, diff

# ------------------------------------------------
# System Object
# ------------------------------------------------

class System:

    def __init__(self,name,domain,structures,mechanisms,math_models):

        self.name=name
        self.domain=domain
        self.structures=structures
        self.mechanisms=mechanisms
        self.math_models=math_models


# ------------------------------------------------
# Base systems
# ------------------------------------------------

BASE_SYSTEMS=[

System(
"Fluid Dynamics",
"physics",
["field","flow"],
["diffusion","feedback","chaos"],
["navier stokes"]
),

System(
"Market Economy",
"economics",
["network"],
["competition","optimization"],
["game theory"]
),

System(
"Neural Networks",
"computer science",
["graph"],
["adaptation","optimization"],
["gradient descent"]
),

System(
"Traffic Networks",
"transport",
["network"],
["diffusion","congestion"],
["flow models"]
),

System(
"Genetic Evolution",
"biology",
["population"],
["selection","mutation"],
["replicator equations"]
),

System(
"Prime Numbers",
"mathematics",
["integer distribution"],
["rarity","filtering"],
["number theory"]
)

]


# ------------------------------------------------
# Synthetic systems
# ------------------------------------------------

PROPERTIES=[
"adaptive","chaotic","distributed",
"competitive","cooperative","dynamic"
]

STRUCTURES=[
"network","graph","field",
"hierarchy","cluster","wave"
]

MECHANISMS=[
"diffusion","competition","selection",
"optimization","feedback","oscillation"
]


def generate_synthetic_systems(n=500):

    systems=[]

    for i in range(n):

        systems.append(

            System(
                f"synthetic_system_{i}",
                "synthetic",
                random.sample(STRUCTURES,1),
                random.sample(MECHANISMS,2),
                []
            )

        )

    return systems


# ------------------------------------------------
# Wikipedia systems
# ------------------------------------------------

def fetch_wikipedia_systems(topic="science"):

    systems=[]

    try:

        url=f"https://en.wikipedia.org/api/rest_v1/page/related/{topic}"

        data=requests.get(url).json()

        for p in data["pages"]:

            name=p["title"]

            systems.append(
                System(
                    name,
                    "wikipedia",
                    random.sample(STRUCTURES,1),
                    random.sample(MECHANISMS,2),
                    []
                )
            )

    except:
        pass

    return systems


# ------------------------------------------------
# OpenAlex research systems
# ------------------------------------------------

def fetch_openalex_systems():

    systems=[]

    try:

        url="https://api.openalex.org/concepts?per-page=20"

        data=requests.get(url).json()

        for c in data["results"]:

            systems.append(
                System(
                    c["display_name"],
                    "research",
                    random.sample(STRUCTURES,1),
                    random.sample(MECHANISMS,2),
                    []
                )
            )

    except:
        pass

    return systems


# ------------------------------------------------
# arXiv research topics
# ------------------------------------------------

def fetch_arxiv_systems():

    systems=[]

    try:

        url="http://export.arxiv.org/api/query?search_query=all:system&max_results=20"

        data=requests.get(url).text

        for i in range(20):

            systems.append(
                System(
                    f"arxiv_topic_{i}",
                    "arxiv",
                    random.sample(STRUCTURES,1),
                    random.sample(MECHANISMS,2),
                    []
                )
            )

    except:
        pass

    return systems


# ------------------------------------------------
# Mechanism matching
# ------------------------------------------------

def match_mechanisms(a,b):

    return list(set(a.mechanisms) & set(b.mechanisms))


# ------------------------------------------------
# Equation generation
# ------------------------------------------------

def derive_equation(mechanisms):

    t=symbols('t')
    x=Function('x')(t)

    if "diffusion" in mechanisms:

        return Eq(diff(x,t),symbols('D')*diff(x,t,2))

    if "optimization" in mechanisms:

        return Eq(diff(x,t),-symbols('eta')*symbols('grad_f'))

    if "competition" in mechanisms:

        return Eq(diff(x,t),symbols('a')*x*(1-x))

    if "selection" in mechanisms:

        return Eq(diff(x,t),symbols('r')*x)

    return Eq(diff(x,t),symbols('f'))


# ------------------------------------------------
# Algorithm suggestion
# ------------------------------------------------

def suggest_algorithm(mechanisms):

    if "diffusion" in mechanisms:

        return "Network diffusion algorithm"

    if "optimization" in mechanisms:

        return "Gradient descent optimization"

    if "competition" in mechanisms:

        return "Game theoretic equilibrium solver"

    if "selection" in mechanisms:

        return "Evolutionary search algorithm"

    return "General dynamical system solver"


# ------------------------------------------------
# Fugue Engine
# ------------------------------------------------

class FugueEngine:

    def __init__(self):

        systems=BASE_SYSTEMS

        systems+=generate_synthetic_systems()

        systems+=fetch_wikipedia_systems()

        systems+=fetch_openalex_systems()

        systems+=fetch_arxiv_systems()

        self.systems=systems


    def discover(self):

        a,b=random.sample(self.systems,2)

        print("\nSYSTEM A:",a.name)
        print("SYSTEM B:",b.name)

        mechanisms=match_mechanisms(a,b)

        print("\nShared mechanisms:",mechanisms)

        equation=derive_equation(mechanisms)

        print("\nDerived math model:")

        print(equation)

        algo=suggest_algorithm(mechanisms)

        print("\nSuggested algorithm:")

        print(algo)


    def solve(self,subject):

        print("\nTARGET SUBJECT:",subject)

        systems=random.sample(self.systems,4)

        mechanisms=[]

        print("\nSystems used:")

        for s in systems:

            print("-",s.name)

            mechanisms+=s.mechanisms

        mechanisms=list(set(mechanisms))

        print("\nExtracted mechanisms:",mechanisms)

        equation=derive_equation(mechanisms)

        print("\nCandidate math:")

        print(equation)

        algo=suggest_algorithm(mechanisms)

        print("\nPossible algorithm:")

        print(algo)


# ------------------------------------------------
# Run
# ------------------------------------------------

if __name__=="__main__":

    engine=FugueEngine()

    print("\n---- RANDOM DISCOVERY ----")

    engine.discover()

    print("\n---- TARGET PROBLEM ----")

    engine.solve("python code analysis")
