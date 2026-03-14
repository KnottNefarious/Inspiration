"""
Neural ODE Learner - Phase 3 (Advanced Feature)
Learns differential equations from time series data

Note: Requires PyTorch. Install with: pip install torch
For simpler use cases, we provide a polynomial fitting fallback
"""

import numpy as np
from typing import Tuple, List, Dict, Optional
import warnings
warnings.filterwarnings('ignore')


# ========================================
# SIMPLE POLYNOMIAL FITTING (No PyTorch needed)
# ========================================

class PolynomialODEFitter:
    """
    Simple ODE learner using polynomial regression
    Doesn't need PyTorch - good for basic cases
    """

    def __init__(self, max_degree: int = 3):
        self.max_degree = max_degree
        self.coefficients = None
        self.equation_string = None


    def fit(self, time: np.ndarray, data: np.ndarray) -> Tuple[np.ndarray, str]:
        """
        Fit polynomial ODE to data

        Args:
            time: Time points (1D array)
            data: Observations (1D array)

        Returns:
            coefficients: Polynomial coefficients
            equation: String representation
        """

        # Estimate derivative using finite differences
        dt = np.diff(time)
        dx = np.diff(data)
        dxdt = dx / dt

        # Use midpoints for x values
        x_mid = (data[:-1] + data[1:]) / 2

        # Fit polynomial: dx/dt = c0 + c1*x + c2*x^2 + ...
        X = np.column_stack([x_mid**i for i in range(self.max_degree + 1)])

        # Least squares fit
        self.coefficients = np.linalg.lstsq(X, dxdt, rcond=None)[0]

        # Build equation string
        self.equation_string = self._build_equation_string()

        return self.coefficients, self.equation_string


    def _build_equation_string(self) -> str:
        """Build human-readable equation string"""

        if self.coefficients is None:
            return "Not fitted"

        terms = []

        for i, coef in enumerate(self.coefficients):
            if abs(coef) < 1e-6:  # Skip near-zero terms
                continue

            if i == 0:
                terms.append(f"{coef:.4f}")
            elif i == 1:
                terms.append(f"{coef:.4f}*x")
            else:
                terms.append(f"{coef:.4f}*x^{i}")

        if not terms:
            return "dx/dt = 0"

        equation = "dx/dt = " + " + ".join(terms)
        return equation.replace("+ -", "- ")


    def predict(self, time: np.ndarray, x0: float) -> np.ndarray:
        """
        Simulate the learned ODE

        Args:
            time: Time points to simulate
            x0: Initial condition

        Returns:
            Predicted trajectory
        """

        if self.coefficients is None:
            raise ValueError("Model not fitted yet")

        # Simple Euler integration
        x = np.zeros(len(time))
        x[0] = x0

        for i in range(len(time) - 1):
            dt = time[i+1] - time[i]

            # Compute dx/dt from polynomial
            dxdt = sum(self.coefficients[j] * x[i]**j 
                      for j in range(len(self.coefficients)))

            x[i+1] = x[i] + dt * dxdt

        return x


    def score(self, time: np.ndarray, data: np.ndarray) -> float:
        """
        Calculate R² score

        Returns:
            R² score (0-1, higher is better)
        """

        predictions = self.predict(time, data[0])

        ss_res = np.sum((data - predictions)**2)
        ss_tot = np.sum((data - np.mean(data))**2)

        r2 = 1 - (ss_res / ss_tot)

        return max(0, min(1, r2))  # Clamp to [0, 1]


# ========================================
# NEURAL ODE LEARNER (Requires PyTorch)
# ========================================

class NeuralODELearner:
    """
    Learn ODEs using Neural Networks
    Requires: pip install torch

    This is a placeholder that shows the architecture.
    Uncomment the code below after installing PyTorch.
    """

    def __init__(self):
        print("[NEURAL ODE] Requires PyTorch")
        print("[FIX] Run: pip install torch")
        print("[NOTE] Using PolynomialODEFitter instead for now")

    def fit(self, time, data):
        print("[INFO] PyTorch not available - use PolynomialODEFitter")
        return None, "PyTorch not installed"

    """
    # UNCOMMENT THIS AFTER INSTALLING PYTORCH:

    def __init__(self, hidden_size: int = 32):
        import torch
        import torch.nn as nn

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Simple neural network: f(x) = dx/dt
        self.net = nn.Sequential(
            nn.Linear(1, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, 1)
        ).to(self.device)

        self.optimizer = torch.optim.Adam(self.net.parameters(), lr=0.01)


    def fit(self, time: np.ndarray, data: np.ndarray, epochs: int = 1000):
        import torch

        # Convert to tensors
        t = torch.from_numpy(time).float().to(self.device)
        x_data = torch.from_numpy(data).float().to(self.device)

        # Training loop
        for epoch in range(epochs):
            self.optimizer.zero_grad()

            # Predict using ODE solver
            x_pred = self._odeint(x_data[0], t)

            # Loss
            loss = torch.mean((x_pred - x_data)**2)

            loss.backward()
            self.optimizer.step()

            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss: {loss.item():.6f}")

        equation = "Learned neural ODE (non-symbolic)"
        return self.net.state_dict(), equation
    """


# ========================================
# ODE LEARNER FACTORY
# ========================================

def learn_ode_from_data(time: np.ndarray, data: np.ndarray, 
                       method: str = "polynomial") -> Dict:
    """
    Learn ODE from time series data

    Args:
        time: Time points (1D array)
        data: Observations (1D array)
        method: "polynomial" (simple, no deps) or "neural" (needs PyTorch)

    Returns:
        Dict with: equation, coefficients, score, predictions
    """

    if method == "polynomial":
        learner = PolynomialODEFitter(max_degree=3)
        coefficients, equation = learner.fit(time, data)
        predictions = learner.predict(time, data[0])
        score = learner.score(time, data)

        return {
            'method': 'polynomial',
            'equation': equation,
            'coefficients': coefficients.tolist(),
            'score': score,
            'predictions': predictions.tolist(),
            'learner': learner
        }

    elif method == "neural":
        try:
            import torch
            learner = NeuralODELearner()
            # Would train here
            return {
                'method': 'neural',
                'equation': 'Neural ODE (install PyTorch to use)',
                'score': 0.0
            }
        except ImportError:
            print("[ERROR] PyTorch not installed")
            print("[FIX] Run: pip install torch")
            print("[INFO] Falling back to polynomial method")
            return learn_ode_from_data(time, data, method="polynomial")

    else:
        raise ValueError(f"Unknown method: {method}")


# ========================================
# MECHANISM CLASSIFICATION
# ========================================

def classify_learned_equation(equation: str, coefficients: np.ndarray) -> List[str]:
    """
    Classify which mechanisms the learned equation exhibits

    Args:
        equation: Equation string
        coefficients: Polynomial coefficients

    Returns:
        List of mechanism names
    """

    mechanisms = []

    # Linear term dominant → selection or diffusion
    if len(coefficients) > 1 and abs(coefficients[1]) > 0.1:
        if coefficients[1] > 0:
            mechanisms.append("selection")
        else:
            mechanisms.append("diffusion")

    # Quadratic term → competition
    if len(coefficients) > 2 and abs(coefficients[2]) > 0.01:
        if coefficients[2] < 0:
            mechanisms.append("competition")

    # Negative feedback
    if len(coefficients) > 1 and coefficients[1] < -0.1:
        mechanisms.append("feedback")

    return mechanisms if mechanisms else ["unknown"]


# ========================================
# TESTING
# ========================================

if __name__ == "__main__":

    print("="*70)
    print("NEURAL ODE LEARNER - TEST")
    print("="*70)

    # Test 1: Logistic growth (competition)
    print("\nTEST 1: Logistic Growth")
    print("-"*70)

    # Generate synthetic data: dx/dt = x(1-x)
    t = np.linspace(0, 10, 100)
    x_true = 1 / (1 + 9*np.exp(-t))  # Analytic solution

    # Add noise
    np.random.seed(42)
    x_data = x_true + np.random.normal(0, 0.02, len(t))

    # Learn ODE
    result = learn_ode_from_data(t, x_data, method="polynomial")

    print(f"Learned equation: {result['equation']}")
    print(f"R² score: {result['score']:.3f}")
    print(f"Coefficients: {result['coefficients']}")

    mechanisms = classify_learned_equation(
        result['equation'],
        np.array(result['coefficients'])
    )
    print(f"Detected mechanisms: {mechanisms}")

    # Test 2: Exponential growth (selection)
    print("\n\nTEST 2: Exponential Growth")
    print("-"*70)

    t = np.linspace(0, 5, 50)
    x_data = 0.1 * np.exp(0.5 * t)
    x_data += np.random.normal(0, 0.01, len(t))

    result = learn_ode_from_data(t, x_data, method="polynomial")

    print(f"Learned equation: {result['equation']}")
    print(f"R² score: {result['score']:.3f}")

    mechanisms = classify_learned_equation(
        result['equation'],
        np.array(result['coefficients'])
    )
    print(f"Detected mechanisms: {mechanisms}")

    print("\n" + "="*70)
    print("Tests complete!")
    print("="*70)
    print("\n[NOTE] For advanced Neural ODE learning:")
    print("  1. Install PyTorch: pip install torch")
    print("  2. Uncomment Neural ODE code in neural_ode_learner.py")
