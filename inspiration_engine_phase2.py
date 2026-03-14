import random
from sympy import symbols, Function, Eq, diff, solve, simplify

from system_database import load_systems
from mechanism_graph import MECHANISM_GRAPH
from enhanced_mechanism_extractor import extract_mechanisms_from_subject
from equation_simulator import EquationSimulator


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
# Evaluate model (ENHANCED with simulation)
# --------------------------------

def evaluate_model(eq, mechanisms, simulator=None):
    """
    Enhanced evaluation using both mathematical properties AND simulation
    """

    # Mathematical properties (Phase 1)
    equilibria = analyze_equilibria(eq)
    sym = detect_symmetry(eq)
    inv = detect_invariants(eq)

    math_score = len(equilibria) + len(sym) + len(inv)
    
    # Simulation validation (Phase 2 - NEW!)
    simulation_score = 0
    simulation_details = None
    
    if simulator is not None:
        eq_str = str(eq)
        sim_score, sim_details = simulator.validate_equation(eq_str, mechanisms)
        simulation_score = sim_score * 10  # Scale to match math_score range
        simulation_details = sim_details
    
    # Combined score (60% simulation, 40% math properties)
    if simulator is not None:
        total_score = (simulation_score * 0.6) + (math_score * 0.4)
    else:
        total_score = math_score

    return total_score, equilibria, sym, inv, simulation_details


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
# Engine (ENHANCED with simulation)
# --------------------------------

class InspirationEngine:

    def __init__(self):

        self.systems = load_systems()
        self.simulator = EquationSimulator()  # NEW: Add simulator

        print("Loaded systems:", len(self.systems))
        print("Simulation validation: ENABLED")


    def search_model(self, subject, verbose=False, use_simulation=True):
        """
        Enhanced search with simulation validation
        """

        # Phase 1: Extract mechanisms
        mechanism_hints = extract_mechanisms_from_subject(subject, verbose=verbose)
        
        if verbose:
            print(f"\n[ENGINE] Extracted mechanisms: {mechanism_hints}")

        candidate_systems = find_relevant_systems(self.systems, mechanism_hints)
        
        if verbose:
            print(f"[ENGINE] Found {len(candidate_systems)} candidate systems")
        
        # FIX: Handle case where we have very few systems
        if len(candidate_systems) < 2:
            if verbose:
                print(f"[ENGINE] WARNING: Only {len(candidate_systems)} candidate systems. Using all systems.")
            candidate_systems = self.systems
        
        if len(candidate_systems) < 2:
            if verbose:
                print(f"[ENGINE] ERROR: Not enough systems in database ({len(self.systems)} total)")
            return None

        best_score = -1
        best_result = None

        # NEW: Use simulator if enabled
        simulator = self.simulator if use_simulation else None
        
        if verbose and use_simulation:
            print(f"[ENGINE] Simulation validation: ENABLED")

        for iteration in range(80):

            # FIX: Don't try to sample more than we have
            max_size = min(4, len(candidate_systems))
            size = random.choice(range(2, max_size + 1))

            systems = random.sample(candidate_systems, size)

            mechanisms = []

            for s in systems:
                mechanisms += s.mechanisms

            mechanisms = list(set(mechanisms))

            eq = compose_equation(mechanisms)

            # NEW: Enhanced evaluation with simulation
            score, equilibria, sym, inv, sim_details = evaluate_model(
                eq, mechanisms, simulator=simulator
            )

            if verbose and iteration < 3:  # Show first few attempts
                print(f"  Attempt {iteration+1}: score={score:.2f}, mechanisms={mechanisms}")
                if sim_details and sim_details.get('simulated'):
                    print(f"    Simulation confidence: {sim_details['confidence']:.2f}")

            if score > best_score:

                best_score = score
                best_result = (systems, mechanisms, eq, equilibria, sym, inv, sim_details)

        if best_result is None:
            return None

        systems, mechanisms, eq, equilibria, sym, inv, sim_details = best_result

        explanation = ""

        if equilibria:
            explanation += f"Equilibria detected: {equilibria}. "

        if sym:
            explanation += f"Symmetry detected: {sym}. "

        if inv:
            explanation += f"Invariants detected: {inv}. "
        
        # NEW: Add simulation info to explanation
        if sim_details and sim_details.get('simulated'):
            confidence = sim_details.get('confidence', 0)
            behaviors = sim_details.get('behaviors', {})
            
            if confidence > 0.7:
                explanation += f"Simulation validates model with {confidence:.0%} confidence. "
            
            active_behaviors = [b for b, present in behaviors.items() if present]
            if active_behaviors:
                explanation += f"Exhibits: {', '.join(active_behaviors)}. "

        model_type = classify_model(mechanisms)

        return systems, mechanisms, eq, equilibria, sym, inv, sim_details, explanation, model_type


    def solve(self, subject, verbose=False, use_simulation=True):
        """
        Enhanced solve with simulation validation
        """

        result = self.search_model(subject, verbose=verbose, use_simulation=use_simulation)

        if result is None:
            return {"analysis": "No meaningful model found."}

        systems, mechanisms, eq, equilibria, sym, inv, sim_details, explanation, model_type = result

        system_names = [s.name for s in systems]

        algo = suggest_algorithm(mechanisms)
        
        # Build response
        response = {
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
        
        # NEW: Add simulation results
        if sim_details:
            response["simulation"] = {
                "validated": sim_details.get('simulated', False),
                "confidence": sim_details.get('confidence', 0),
                "behaviors": sim_details.get('behaviors', {})
            }
            
            # Include trajectory for plotting (if not too large)
            if 'trajectory' in sim_details:
                response["simulation"]["trajectory"] = sim_details['trajectory']
                response["simulation"]["time"] = sim_details['time']

        return response


    def discovery_mode(self):

        return self.solve("general discovery")
        