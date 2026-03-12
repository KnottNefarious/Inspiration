import random
from sympy import symbols, Function, Eq, diff, solve, simplify

from system_database import load_systems
from mechanism_graph import MECHANISM_GRAPH
from enhanced_mechanism_extractor import extract_mechanisms_from_subject


# --------------------------------
# Find systems with those mechanisms
# --------------------------------

def find_relevant_systems(systems, mechanism_hints):

    relevant = []

    for s in systems:

        if any(m in s.mechanisms for m in mechanism_hints):
            relevant.append(s)

    if len(relevant) < 2:
        return systems

    return relevant


# --------------------------------
# Compose equation from mechanisms
# --------------------------------

def compose_equation(mechanisms):

    t = symbols('t')
    x = Function('x')(t)

    rhs = 0

    if "diffusion" in mechanisms:
        D = symbols('D')
        rhs += D * diff(x, t, 2)

    if "optimization" in mechanisms:
        eta, grad_f = symbols('eta grad_f')
        rhs += -eta * grad_f

    if "competition" in mechanisms:
        a = symbols('a')
        rhs += a * x * (1 - x)

    if "selection" in mechanisms:
        r = symbols('r')
        rhs += r * x

    if "feedback" in mechanisms:
        k = symbols('k')
        rhs += k * x

    if rhs == 0:
        rhs = symbols('f')

    return Eq(diff(x, t), rhs)


# --------------------------------
# Equilibria detection (safe)
# --------------------------------

def analyze_equilibria(eq):

    t = symbols('t')
    x = symbols('x')

    try:

        rhs = eq.rhs.subs({Function('x')(t): x})

        if rhs.is_polynomial(x):

            equilibria = solve(rhs, x)

            return equilibria

        else:

            return []

    except:

        return []


# --------------------------------
# Symmetry detection
# --------------------------------

def detect_symmetry(eq):

    t = symbols('t')
    x = symbols('x')

    rhs = eq.rhs.subs({Function('x')(t): x})

    sym = []

    try:

        if simplify(rhs.subs(x, -x) + rhs) == 0:
            sym.append("sign symmetry")

    except:

        pass

    return sym


# --------------------------------
# Invariant detection
# --------------------------------

def detect_invariants(eq):

    t = symbols('t')
    x = symbols('x')

    rhs = eq.rhs.subs({Function('x')(t): x})

    invariants = []

    try:

        if simplify(rhs.subs(x, 0)) == 0:
            invariants.append("x = 0 invariant")

    except:

        pass

    return invariants


# --------------------------------
# Evaluate model
# --------------------------------

def evaluate_model(eq):

    equilibria = analyze_equilibria(eq)
    sym = detect_symmetry(eq)
    inv = detect_invariants(eq)

    score = len(equilibria) + len(sym) + len(inv)

    return score, equilibria, sym, inv


# --------------------------------
# Model classification
# --------------------------------

def classify_model(mechanisms):

    if "diffusion" in mechanisms and "competition" in mechanisms:
        return "Reaction–Diffusion System"

    if "optimization" in mechanisms and "diffusion" in mechanisms:
        return "Diffusion Optimization System"

    if "competition" in mechanisms and "selection" in mechanisms:
        return "Replicator Dynamics"

    if "feedback" in mechanisms and "optimization" in mechanisms:
        return "Adaptive Control System"

    if "diffusion" in mechanisms:
        return "Diffusion System"

    return "General Dynamical System"


# --------------------------------
# Suggest algorithm
# --------------------------------

def suggest_algorithm(mechanisms):

    if "diffusion" in mechanisms and "optimization" in mechanisms:
        return "Diffusion Optimization Algorithm"

    if "competition" in mechanisms and "selection" in mechanisms:
        return "Evolutionary Game Algorithm"

    if "diffusion" in mechanisms:
        return "Network Diffusion Algorithm"

    return "General Dynamical Solver"


# --------------------------------
# Engine
# --------------------------------

class InspirationEngine:

    def __init__(self):

        self.systems = load_systems()

        print("Loaded systems:", len(self.systems))


    def search_model(self, subject, verbose=False):

        # NEW: Enhanced mechanism extraction
        mechanism_hints = extract_mechanisms_from_subject(subject, verbose=verbose)

        if verbose:
            print(f"\n[ENGINE] Extracted mechanisms: {mechanism_hints}")

        candidate_systems = find_relevant_systems(self.systems, mechanism_hints)

        if verbose:
            print(f"[ENGINE] Found {len(candidate_systems)} candidate systems")

        best_score = -1
        best_result = None

        for _ in range(80):

            size = random.choice([2,3,4])

            systems = random.sample(candidate_systems, size)

            mechanisms = []

            for s in systems:
                mechanisms += s.mechanisms

            mechanisms = list(set(mechanisms))

            eq = compose_equation(mechanisms)

            score, equilibria, sym, inv = evaluate_model(eq)

            if score > best_score:

                best_score = score
                best_result = (systems, mechanisms, eq, equilibria, sym, inv)

        if best_result is None:
            return None

        systems, mechanisms, eq, equilibria, sym, inv = best_result

        explanation = ""

        if equilibria:
            explanation += f"Equilibria detected: {equilibria}. "

        if sym:
            explanation += f"Symmetry detected: {sym}. "

        if inv:
            explanation += f"Invariants detected: {inv}. "

        model_type = classify_model(mechanisms)

        return systems, mechanisms, eq, equilibria, sym, inv, explanation, model_type


    def solve(self, subject, verbose=False):

        result = self.search_model(subject, verbose=verbose)

        if result is None:
            return {"analysis": "No meaningful model found."}

        systems, mechanisms, eq, equilibria, sym, inv, explanation, model_type = result

        system_names = [s.name for s in systems]

        algo = suggest_algorithm(mechanisms)

        return {

            "subject": subject,
            "systems": system_names,
            "mechanisms": mechanisms,
            "equation": str(eq),
            "algorithm": algo,
            "analysis": explanation,
            "equilibria": equilibria,
            "symmetries": sym,
            "invariants": inv,
            "model_type": model_type
        }


    def discovery_mode(self):

        return self.solve("general discovery")
