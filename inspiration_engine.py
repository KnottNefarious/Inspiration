import random
from sympy import symbols, Function, Eq, diff

from system_database import load_systems, save_systems
from research_fetcher import fetch_arxiv_systems


# ----------------------------------------
# Mechanism Matching
# ----------------------------------------

def match_mechanisms(a, b):

    return list(set(a.mechanisms) & set(b.mechanisms))


# ----------------------------------------
# Equation Generator
# ----------------------------------------

def derive_equation(mechanisms):

    t = symbols('t')
    x = Function('x')(t)

    if "diffusion" in mechanisms:

        return Eq(diff(x, t), symbols('D') * diff(x, t, 2))

    if "optimization" in mechanisms:

        return Eq(diff(x, t), -symbols('eta') * symbols('grad_f'))

    if "competition" in mechanisms:

        return Eq(diff(x, t), symbols('a') * x * (1 - x))

    if "selection" in mechanisms:

        return Eq(diff(x, t), symbols('r') * x)

    if "feedback" in mechanisms:

        return Eq(diff(x, t), symbols('k') * x)

    return Eq(diff(x, t), symbols('f'))


# ----------------------------------------
# Algorithm Suggestions
# ----------------------------------------

def suggest_algorithm(mechanisms):

    if "diffusion" in mechanisms:

        return "Network diffusion algorithm"

    if "optimization" in mechanisms:

        return "Gradient descent optimization"

    if "competition" in mechanisms:

        return "Game theoretic equilibrium solver"

    if "selection" in mechanisms:

        return "Evolutionary search algorithm"

    if "feedback" in mechanisms:

        return "Control system feedback solver"

    return "Generic dynamical system solver"


# ----------------------------------------
# Inspiration Engine
# ----------------------------------------

class InspirationEngine:

    def __init__(self):

        self.systems = load_systems()

        print("Loaded systems:", len(self.systems))


    # ------------------------------------
    # Learn systems from research papers
    # ------------------------------------

    def learn_from_research(self):

        new_systems = fetch_arxiv_systems()

        print("New systems discovered:", len(new_systems))

        self.systems.extend(new_systems)

        save_systems(self.systems)


    # ------------------------------------
    # Random discovery mode
    # ------------------------------------

    def discover(self):

        if len(self.systems) < 2:
            return "Not enough systems in database."

        a, b = random.sample(self.systems, 2)

        mechanisms = match_mechanisms(a, b)

        eq = derive_equation(mechanisms)

        algo = suggest_algorithm(mechanisms)

        result = {
            "systemA": a.name,
            "systemB": b.name,
            "mechanisms": mechanisms,
            "equation": str(eq),
            "algorithm": algo
        }

        return result


    # ------------------------------------
    # Target problem solving mode
    # ------------------------------------

    def solve(self, subject):

        if len(self.systems) < 4:
            return {
                "subject": subject,
                "systems": [],
                "mechanisms": [],
                "equation": "Not enough systems in database",
                "algorithm": ""
            }

        systems = random.sample(self.systems, 4)

        mechanisms = []

        system_names = []

        for s in systems:

            system_names.append(s.name)

            mechanisms += s.mechanisms

        mechanisms = list(set(mechanisms))

        eq = derive_equation(mechanisms)

        algo = suggest_algorithm(mechanisms)

        return {

            "subject": subject,

            "systems": system_names,

            "mechanisms": mechanisms,

            "equation": str(eq),

            "algorithm": algo
        }


# ----------------------------------------
# Standalone run mode (for testing)
# ----------------------------------------

if __name__ == "__main__":

    engine = InspirationEngine()

    engine.learn_from_research()

    result = engine.discover()

    print("\nDiscovery Mode Result\n")

    print(result)

    result2 = engine.solve("python code analysis")

    print("\nTarget Mode Result\n")

    print(result2)
