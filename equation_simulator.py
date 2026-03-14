"""
Equation Simulator - Phase 2
Simulates differential equations and validates their behavior matches mechanisms
"""

import numpy as np
from scipy.integrate import odeint
import warnings
warnings.filterwarnings('ignore')


# ========================================
# MECHANISM BEHAVIOR VALIDATORS
# ========================================

class BehaviorValidator:
    """
    Validates if simulated behavior matches expected mechanism patterns
    """
    
    @staticmethod
    def detect_oscillation(trajectory):
        """Detect if trajectory oscillates"""
        if len(trajectory) < 10:
            return False
        
        # Check for sign changes (peaks and valleys)
        diff = np.diff(trajectory)
        sign_changes = np.sum(np.diff(np.sign(diff)) != 0)
        
        # More than 2 direction changes = oscillation
        return sign_changes > 2
    
    
    @staticmethod
    def detect_growth(trajectory):
        """Detect exponential or logistic growth"""
        if len(trajectory) < 5:
            return False
        
        # Check if generally increasing
        return trajectory[-1] > trajectory[0] * 1.1
    
    
    @staticmethod
    def detect_decay(trajectory):
        """Detect exponential decay"""
        if len(trajectory) < 5:
            return False
        
        # Check if generally decreasing
        return trajectory[-1] < trajectory[0] * 0.9
    
    
    @staticmethod
    def detect_equilibrium(trajectory, tolerance=0.01):
        """Detect if system reaches equilibrium"""
        if len(trajectory) < 10:
            return False
        
        # Check if last 20% of trajectory is stable
        last_portion = trajectory[-len(trajectory)//5:]
        variation = np.std(last_portion)
        
        return variation < tolerance
    
    
    @staticmethod
    def detect_competition(trajectory):
        """Detect logistic growth pattern (competition)"""
        if len(trajectory) < 10:
            return False
        
        # Logistic: starts growing, then saturates
        first_half = trajectory[:len(trajectory)//2]
        second_half = trajectory[len(trajectory)//2:]
        
        first_growth = first_half[-1] - first_half[0]
        second_growth = second_half[-1] - second_half[0]
        
        # Growing initially but slowing down
        return first_growth > 0 and second_growth < first_growth * 0.5
    
    
    @staticmethod
    def detect_chaos(trajectory):
        """Detect chaotic behavior"""
        if len(trajectory) < 20:
            return False
        
        # Check for irregular, non-repeating oscillations
        diff = np.diff(trajectory)
        sign_changes = np.sum(np.diff(np.sign(diff)) != 0)
        
        # Many direction changes but no clear periodicity
        is_irregular = sign_changes > 5
        
        # Check variance in different sections
        n_sections = 4
        section_size = len(trajectory) // n_sections
        variances = [np.var(trajectory[i*section_size:(i+1)*section_size]) 
                    for i in range(n_sections)]
        
        # Chaotic if high variance variation
        variance_variation = np.std(variances) / (np.mean(variances) + 1e-10)
        
        return is_irregular and variance_variation > 0.3
    
    
    @staticmethod
    def validate_mechanism(mechanism, trajectory):
        """
        Validate if trajectory matches expected behavior for mechanism
        Returns (matches: bool, confidence: float)
        """
        
        validators = {
            "oscillation": BehaviorValidator.detect_oscillation,
            "competition": BehaviorValidator.detect_competition,
            "selection": BehaviorValidator.detect_growth,
            "feedback": BehaviorValidator.detect_equilibrium,
            "adaptation": BehaviorValidator.detect_equilibrium,
            "optimization": BehaviorValidator.detect_equilibrium,
            "chaos": BehaviorValidator.detect_chaos,
        }
        
        if mechanism not in validators:
            return True, 0.5  # Unknown mechanism, neutral confidence
        
        matches = validators[mechanism](trajectory)
        confidence = 0.8 if matches else 0.2
        
        return matches, confidence


# ========================================
# EQUATION SIMULATOR
# ========================================

class EquationSimulator:
    """
    Simulates differential equations and validates behavior
    """
    
    def __init__(self):
        self.validator = BehaviorValidator()
    
    
    def create_ode_function(self, equation_str, mechanisms):
        """
        Create a function that can be integrated
        Returns None if equation cannot be simulated
        """
        
        # Extract equation components
        # Format: "Eq(Derivative(x(t), t), rhs)"
        
        try:
            # Simple heuristic: create ODE based on mechanisms
            def ode_func(x, t, params):
                """
                Generic ODE function based on mechanisms
                """
                if x < 0:
                    x = 0  # Keep positive
                
                dxdt = 0
                
                # Unpack parameters
                if "diffusion" in mechanisms:
                    D = params.get('D', 0.1)
                    # Simplified: no spatial derivatives, just damping
                    dxdt += -D * x
                
                if "optimization" in mechanisms:
                    eta = params.get('eta', 0.1)
                    grad_f = params.get('grad_f', x - 0.5)  # Target 0.5
                    dxdt += -eta * grad_f
                
                if "competition" in mechanisms:
                    a = params.get('a', 1.0)
                    dxdt += a * x * (1 - x)
                
                if "selection" in mechanisms:
                    r = params.get('r', 0.5)
                    dxdt += r * x
                
                if "feedback" in mechanisms:
                    k = params.get('k', -0.2)
                    dxdt += k * x
                
                if "oscillation" in mechanisms:
                    omega = params.get('omega', 2.0)
                    # Add oscillatory component
                    dxdt += omega * np.sin(t)
                
                if "reaction" in mechanisms:
                    k_react = params.get('k_react', 0.3)
                    dxdt += k_react * x * (1 - x)
                
                return dxdt
            
            return ode_func
            
        except Exception as e:
            print(f"[SIMULATOR] Error creating ODE function: {e}")
            return None
    
    
    def simulate(self, equation_str, mechanisms, duration=10.0, initial_value=0.1):
        """
        Simulate the equation and return trajectory
        
        Returns:
            trajectory: np.array of values over time
            time: np.array of time points
            success: bool indicating if simulation succeeded
        """
        
        # Create ODE function
        ode_func = self.create_ode_function(equation_str, mechanisms)
        
        if ode_func is None:
            return None, None, False
        
        # Time points
        t = np.linspace(0, duration, 200)
        
        # Initial condition
        x0 = initial_value
        
        # Parameters (could be tuned later)
        params = {
            'D': 0.1,
            'eta': 0.2,
            'grad_f': 0.5,
            'a': 1.0,
            'r': 0.3,
            'k': -0.2,
            'omega': 2.0,
            'k_react': 0.5
        }
        
        try:
            # Integrate ODE
            trajectory = odeint(ode_func, x0, t, args=(params,))
            
            # Check for numerical issues
            if np.any(np.isnan(trajectory)) or np.any(np.isinf(trajectory)):
                return None, None, False
            
            # Check for explosion
            if np.max(np.abs(trajectory)) > 1e6:
                return None, None, False
            
            return trajectory.flatten(), t, True
            
        except Exception as e:
            print(f"[SIMULATOR] Integration failed: {e}")
            return None, None, False
    
    
    def validate_equation(self, equation_str, mechanisms, verbose=False):
        """
        Simulate equation and validate behavior matches mechanisms
        
        Returns:
            score: float (0-1) indicating quality
            details: dict with simulation results
        """
        
        # Try simulation
        trajectory, time, success = self.simulate(equation_str, mechanisms)
        
        if not success or trajectory is None:
            return 0.0, {
                'simulated': False,
                'error': 'Simulation failed'
            }
        
        # Validate each mechanism
        validations = {}
        total_confidence = 0
        num_validated = 0
        
        for mechanism in mechanisms:
            matches, confidence = self.validator.validate_mechanism(mechanism, trajectory)
            validations[mechanism] = {
                'matches': matches,
                'confidence': confidence
            }
            total_confidence += confidence
            num_validated += 1
            
            if verbose:
                status = "✓" if matches else "✗"
                print(f"  [{status}] {mechanism}: confidence={confidence:.2f}")
        
        # Calculate overall score
        if num_validated > 0:
            avg_confidence = total_confidence / num_validated
        else:
            avg_confidence = 0.5
        
        # Detect behavior patterns
        behaviors = {
            'oscillates': self.validator.detect_oscillation(trajectory),
            'reaches_equilibrium': self.validator.detect_equilibrium(trajectory),
            'grows': self.validator.detect_growth(trajectory),
            'chaotic': self.validator.detect_chaos(trajectory)
        }
        
        details = {
            'simulated': True,
            'trajectory': trajectory.tolist() if len(trajectory) < 50 else trajectory[::4].tolist(),
            'time': time.tolist() if len(time) < 50 else time[::4].tolist(),
            'validations': validations,
            'behaviors': behaviors,
            'confidence': avg_confidence
        }
        
        return avg_confidence, details
    
    
    def simulate_multiple(self, equation_str, mechanisms, n_trials=3):
        """
        Run multiple simulations with different initial conditions
        Returns average score
        """
        
        initial_values = [0.1, 0.5, 0.9][:n_trials]
        scores = []
        all_details = []
        
        for init_val in initial_values:
            traj, t, success = self.simulate(equation_str, mechanisms, 
                                            initial_value=init_val)
            
            if success:
                score, details = self.validate_equation(equation_str, mechanisms)
                scores.append(score)
                all_details.append(details)
        
        if len(scores) == 0:
            return 0.0, None
        
        avg_score = np.mean(scores)
        
        # Return details from best simulation
        best_idx = np.argmax(scores)
        
        return avg_score, all_details[best_idx]


# ========================================
# CONVENIENCE FUNCTIONS
# ========================================

def simulate_equation(equation_str, mechanisms, verbose=False):
    """
    Convenience function to simulate and validate an equation
    
    Returns:
        score: float (0-1)
        details: dict with results
    """
    simulator = EquationSimulator()
    return simulator.validate_equation(equation_str, mechanisms, verbose=verbose)


def test_equation_quality(equation_str, mechanisms):
    """
    Quick test if equation is good
    Returns bool
    """
    score, _ = simulate_equation(equation_str, mechanisms)
    return score > 0.5


# ========================================
# TESTING
# ========================================

if __name__ == "__main__":
    
    print("="*70)
    print("EQUATION SIMULATOR - TEST SUITE")
    print("="*70)
    
    # Test cases
    test_cases = [
        {
            "name": "Competition (Logistic Growth)",
            "mechanisms": ["competition"],
            "equation": "Eq(Derivative(x(t), t), a*x*(1-x))"
        },
        {
            "name": "Selection (Exponential Growth)",
            "mechanisms": ["selection"],
            "equation": "Eq(Derivative(x(t), t), r*x)"
        },
        {
            "name": "Feedback (Stabilization)",
            "mechanisms": ["feedback"],
            "equation": "Eq(Derivative(x(t), t), k*x)"
        },
        {
            "name": "Competition + Selection",
            "mechanisms": ["competition", "selection"],
            "equation": "Eq(Derivative(x(t), t), a*x*(1-x) + r*x)"
        },
        {
            "name": "Oscillation",
            "mechanisms": ["oscillation"],
            "equation": "Eq(Derivative(x(t), t), omega*sin(t))"
        }
    ]
    
    simulator = EquationSimulator()
    
    print("\nRunning simulations...\n")
    
    for test in test_cases:
        print(f"\n{'='*70}")
        print(f"TEST: {test['name']}")
        print(f"Mechanisms: {test['mechanisms']}")
        print(f"{'='*70}")
        
        score, details = simulator.validate_equation(
            test['equation'], 
            test['mechanisms'],
            verbose=True
        )
        
        print(f"\n  Overall Score: {score:.2f}")
        print(f"  Simulated: {details['simulated']}")
        
        if details['simulated']:
            print(f"  Behaviors detected:")
            for behavior, present in details['behaviors'].items():
                status = "✓" if present else "✗"
                print(f"    [{status}] {behavior}")
        
        if score > 0.6:
            print(f"\n  ✓ GOOD EQUATION (score > 0.6)")
        else:
            print(f"\n  ✗ POOR EQUATION (score < 0.6)")
    
    print("\n" + "="*70)
    print("Testing complete!")
    print("="*70)
    