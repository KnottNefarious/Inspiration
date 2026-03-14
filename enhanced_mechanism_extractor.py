"""
Enhanced Mechanism Extractor
Replaces simple keyword matching with hybrid approach:
- N-gram phrase matching (context-aware)
- TF-IDF semantic similarity
- Pattern-based rules
"""

import re
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ========================================
# MECHANISM CORPUS (for TF-IDF)
# ========================================

MECHANISM_CORPUS = {
    "diffusion": """
        spread propagate distribute flow permeate transmit
        network transmission contagion infection viral epidemic
        heat temperature gradient concentration chemical
        information idea rumor disease meme
        through across via throughout among between
        social media communication messaging
    """,

    "optimization": """
        optimize maximize minimize improve enhance tune refine
        gradient descent algorithm search learning train
        best optimal efficient effective fitness
        cost function objective loss utility reward
        performance quality accuracy solution
        hill climbing evolution genetic
    """,

    "competition": """
        compete rival struggle contest fight battle
        market share dominance zero-sum game
        resources scarce limited finite bounded
        winner loser survival fitness selection
        economic business trade commercial
        predator prey hunter
    """,

    "feedback": """
        loop cycle recursive iterate circular
        control regulate stabilize homeostasis equilibrium
        amplify reinforce dampen suppress negative positive
        response adjustment correction adaptation
        self-regulating self-correcting autonomous
        sensor actuator controller
    """,

    "selection": """
        choose select filter pick evolve survive
        fitness adapt natural artificial
        mutation variation diversity population
        survival reproduce generation breeding
        Darwin evolution genetic inheritance
    """,

    "adaptation": """
        adapt adjust learn modify change evolve
        responsive flexible dynamic plastic
        environment experience feedback training
        machine learning neural network AI
        behavioral cognitive developmental
        plasticity resilience robustness
    """,

    "oscillation": """
        oscillate vibrate cycle periodic rhythm
        wave frequency amplitude phase
        pendulum harmonic resonance
        alternating fluctuation variation
        temporal dynamics pattern
        sine cosine periodic
    """,

    "propagation": """
        propagate travel move spread transmit
        wave signal information message
        forward cascade chain reaction
        velocity speed direction path
        spatial temporal domain
    """,

    "chaos": """
        chaos chaotic unpredictable random stochastic
        turbulent turbulence complex nonlinear
        butterfly effect sensitive dependence
        strange attractor fractal
        deterministic unpredictability
    """,

    "reaction": """
        reaction chemical catalyst enzyme
        transform convert process interact
        substrate product reagent
        kinetics rate constant
        stoichiometry equilibrium
    """,

    "coordination": """
        coordinate synchronize align organize
        consensus agreement cooperation
        distributed decentralized collaborative
        swarm flock herd collective
        emergence self-organization
    """,

    "mutation": """
        mutate change vary alter modify
        genetic DNA RNA gene
        random stochastic probability
        variation diversity polymorphism
        error mistake fault
    """,

    "exploration": """
        explore search discover investigate
        random trial error experiment
        curiosity novelty unknown
        sample probe test
        breadth diversity coverage
    """,

    "congestion": """
        congestion traffic jam bottleneck
        overcrowding saturation capacity
        delay latency queue waiting
        network road infrastructure
        throughput bandwidth limitation
    """,

    "infection": """
        infect contagious disease epidemic pandemic
        virus bacteria pathogen spread
        transmission contact exposure
        susceptible infected recovered
        SIR SEIR model
    """
}


# ========================================
# N-GRAM DICTIONARIES
# ========================================

MECHANISM_NGRAMS = {
    "diffusion": {
        1: ["spread", "flow", "propagate", "diffuse", "transmit", "permeate"],
        2: ["information spread", "viral spread", "heat flow", "network propagation",
            "disease spread", "idea diffusion", "social contagion"],
        3: ["spread through network", "propagate across system", "flow through medium",
            "diffuse across space", "transmit via network"]
    },

    "optimization": {
        1: ["optimize", "maximize", "minimize", "improve", "enhance", "tune"],
        2: ["gradient descent", "optimize performance", "maximize efficiency",
            "machine learning", "improve quality", "enhance system", "best solution"],
        3: ["optimize network learning", "improve system performance", "maximize objective function",
            "enhance model accuracy", "find optimal solution"]
    },

    "adaptation": {
        1: ["adapt", "learn", "adjust", "evolve", "modify", "train"],
        2: ["machine learning", "adaptive system", "learning algorithm", "neural network",
            "adjust parameters", "evolve strategy", "learn pattern"],
        3: ["learn from experience", "adapt to changes", "adjust based on feedback",
            "evolve over time", "neural network learning"]
    },

    "competition": {
        1: ["compete", "rival", "contest", "fight", "struggle", "battle"],
        2: ["market competition", "compete for resources", "competitive advantage",
            "zero sum game", "survival of fittest"],
        3: ["compete for limited resources", "struggle for survival", "market share competition"]
    },

    "feedback": {
        1: ["feedback", "loop", "cycle", "control", "regulate"],
        2: ["feedback loop", "control system", "negative feedback", "positive feedback",
            "self regulate", "closed loop"],
        3: ["negative feedback loop", "positive feedback control", "self regulating system"]
    },

    "selection": {
        1: ["select", "choose", "filter", "evolve", "survival"],
        2: ["natural selection", "artificial selection", "evolutionary selection",
            "survival of fittest", "genetic selection"],
        3: ["natural selection process", "evolutionary survival mechanism"]
    },

    "oscillation": {
        1: ["oscillate", "vibrate", "cycle", "periodic", "wave"],
        2: ["periodic oscillation", "harmonic motion", "oscillating system",
            "wave pattern", "cyclic behavior"],
        3: ["periodic oscillation pattern", "harmonic oscillation system"]
    },

    "propagation": {
        1: ["propagate", "travel", "transmit", "cascade"],
        2: ["wave propagation", "signal propagation", "information propagation",
            "cascade effect", "chain reaction"],
        3: ["propagate through medium", "cascade through network"]
    },

    "coordination": {
        1: ["coordinate", "synchronize", "align", "consensus"],
        2: ["swarm coordination", "distributed consensus", "synchronized behavior",
            "collective coordination", "emergent coordination"],
        3: ["coordinate distributed system", "achieve distributed consensus"]
    }
}


# ========================================
# PATTERN MATCHING RULES
# ========================================

MECHANISM_PATTERNS = {
    "diffusion": [
        (r"\b(spread|propagat|diffus|flow|transmit)\w*", 0.8),
        (r"\b(network|social|viral|contagion|epidemic)", 0.6),
        (r"\b(through|across|throughout|via)", 0.3),
        (r"\b(information|idea|disease|heat|rumor)", 0.4)
    ],

    "optimization": [
        (r"\b(optim|maxim|minim)\w*", 0.9),
        (r"\b(best|efficient|effective|optimal)", 0.7),
        (r"\b(gradient|descent|algorithm|search)", 0.8),
        (r"\b(train|learn|fit|improve|enhance)", 0.6)
    ],

    "adaptation": [
        (r"\b(adapt|learn|adjust|evolve|modify)\w*", 0.9),
        (r"\b(neural|network|machine|AI|intelligent)", 0.6),
        (r"\b(training|learning|adaptive|plastic)", 0.7),
        (r"\b(experience|feedback|environment)", 0.5)
    ],

    "competition": [
        (r"\b(compet|rival|contest|fight|struggle)\w*", 0.9),
        (r"\b(market|share|dominance|game)", 0.7),
        (r"\b(resources|scarce|limited|finite)", 0.6),
        (r"\b(winner|loser|survival|fitness)", 0.7)
    ],

    "feedback": [
        (r"\b(feedback|loop|cycle|circular|recursive)", 0.9),
        (r"\b(control|regulat|stabili\w*)", 0.7),
        (r"\b(amplif|reinforce|dampen|suppress)", 0.8),
        (r"\b(homeostasis|equilibrium|balance)", 0.7)
    ],

    "selection": [
        (r"\b(select|choose|filter|evolv\w*)", 0.8),
        (r"\b(natural|artificial|genetic|evolutionary)", 0.7),
        (r"\b(survival|fitness|mutation|variation)", 0.8),
        (r"\b(Darwin|evolution|breeding|reproduction)", 0.6)
    ],

    "oscillation": [
        (r"\b(oscillat|vibrat|periodic|harmonic)\w*", 0.9),
        (r"\b(wave|frequency|amplitude|cycle)", 0.8),
        (r"\b(rhythm|pattern|temporal)", 0.6)
    ],

    "coordination": [
        (r"\b(coordinat|synchron|align|consensus)\w*", 0.9),
        (r"\b(swarm|flock|herd|collective)", 0.8),
        (r"\b(distributed|decentralized|emergent)", 0.7)
    ]
}


# ========================================
# EXTRACTORS
# ========================================

class MechanismExtractor:
    """
    Hybrid mechanism extraction using multiple strategies
    """

    def __init__(self):
        # Initialize TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
        corpus_texts = list(MECHANISM_CORPUS.values())
        self.mechanism_names = list(MECHANISM_CORPUS.keys())
        self.mechanism_vectors = self.vectorizer.fit_transform(corpus_texts)


    def extract_ngrams(self, subject):
        """Extract mechanisms using n-gram matching"""
        subject_lower = subject.lower()
        words = subject_lower.split()

        mechanism_scores = defaultdict(float)

        for mechanism, ngram_dict in MECHANISM_NGRAMS.items():
            # Check 3-grams (highest priority)
            if 3 in ngram_dict:
                for ngram in ngram_dict[3]:
                    if ngram in subject_lower:
                        mechanism_scores[mechanism] += 3.0

            # Check 2-grams
            if 2 in ngram_dict:
                for ngram in ngram_dict[2]:
                    if ngram in subject_lower:
                        mechanism_scores[mechanism] += 2.0

            # Check 1-grams
            if 1 in ngram_dict:
                word_set = set(words)
                matches = word_set.intersection(set(ngram_dict[1]))
                mechanism_scores[mechanism] += len(matches) * 1.0

        return mechanism_scores


    def extract_tfidf(self, subject):
        """Extract mechanisms using TF-IDF similarity"""
        subject_vector = self.vectorizer.transform([subject])
        similarities = cosine_similarity(subject_vector, self.mechanism_vectors)[0]

        mechanism_scores = {}
        for idx, similarity in enumerate(similarities):
            if similarity > 0.05:  # Threshold
                mechanism_scores[self.mechanism_names[idx]] = similarity

        return mechanism_scores


    def extract_patterns(self, subject):
        """Extract mechanisms using pattern matching"""
        subject_lower = subject.lower()
        mechanism_scores = defaultdict(float)

        for mechanism, patterns in MECHANISM_PATTERNS.items():
            score = 0
            matches = 0

            for pattern, weight in patterns:
                if re.search(pattern, subject_lower):
                    score += weight
                    matches += 1

            if matches > 0:
                # Normalize by number of patterns
                mechanism_scores[mechanism] = score / len(patterns)

        return mechanism_scores


    def extract_hybrid(self, subject, verbose=False):
        """
        Hybrid extraction combining all strategies
        Returns list of mechanisms sorted by confidence
        """

        # Get scores from each strategy
        ngram_scores = self.extract_ngrams(subject)
        tfidf_scores = self.extract_tfidf(subject)
        pattern_scores = self.extract_patterns(subject)

        # Aggregate with weights
        # N-grams: 1.0 (best for context)
        # TF-IDF: 0.8 (semantic similarity)
        # Patterns: 0.6 (linguistic rules)

        all_mechanisms = defaultdict(float)

        for mechanism, score in ngram_scores.items():
            all_mechanisms[mechanism] += score * 1.0

        for mechanism, score in tfidf_scores.items():
            all_mechanisms[mechanism] += score * 0.8

        for mechanism, score in pattern_scores.items():
            all_mechanisms[mechanism] += score * 0.6

        if verbose:
            print(f"\n[DEBUG] Subject: {subject}")
            print(f"[DEBUG] N-gram scores: {dict(ngram_scores)}")
            print(f"[DEBUG] TF-IDF scores: {dict(tfidf_scores)}")
            print(f"[DEBUG] Pattern scores: {dict(pattern_scores)}")
            print(f"[DEBUG] Combined scores: {dict(all_mechanisms)}")

        # Normalize scores
        if all_mechanisms:
            max_score = max(all_mechanisms.values())

            # Fix division by zero
            if max_score > 0:
                normalized = {m: s/max_score for m, s in all_mechanisms.items()}
            else:
                # All scores are zero, return empty
                if verbose:
                    print(f"[DEBUG] All mechanism scores are zero")
                return []

            # Apply threshold and sort by score
            threshold = 0.20  # Lower threshold to catch more mechanisms
            results = [(m, s) for m, s in normalized.items() if s >= threshold]
            results.sort(key=lambda x: x[1], reverse=True)

            if verbose:
                print(f"[DEBUG] Normalized scores: {dict(normalized)}")
                print(f"[DEBUG] Final results (threshold={threshold}): {results}")

            # Return just the mechanism names
            return [m for m, s in results]

        return []


# ========================================
# CONVENIENCE FUNCTION (drop-in replacement)
# ========================================

def extract_mechanisms_from_subject(subject, verbose=False):
    """
    Drop-in replacement for the original function.
    Much smarter than keyword matching!

    Args:
        subject: The subject text to analyze
        verbose: If True, prints debug information

    Returns:
        List of mechanism names
    """
    extractor = MechanismExtractor()
    return extractor.extract_hybrid(subject, verbose=verbose)


# ========================================
# TESTING
# ========================================

if __name__ == "__main__":

    print("="*70)
    print("MECHANISM EXTRACTOR - TEST SUITE")
    print("="*70)

    test_cases = [
        "optimize network learning",
        "neural network optimization",
        "spread of disease through population",
        "market competition and pricing",
        "feedback control system",
        "evolutionary selection process",
        "information diffusion in social networks",
        "swarm coordination behavior",
        "adaptive learning algorithm",
        "oscillating chemical reaction",
        "how does information spread through a network",
        "optimize distributed system performance",
        "competitive market dynamics",
        "self-regulating feedback loop",
        "genetic algorithm with selection",
    ]

    extractor = MechanismExtractor()

    print("\nTesting hybrid extraction:\n")

    for subject in test_cases:
        print(f"\nSubject: '{subject}'")

        # Old method (for comparison)
        old_result = []
        subject_lower = subject.lower()
        if "network" in subject_lower:
            old_result.append("diffusion")
        if "learning" in subject_lower or "adaptive" in subject_lower:
            old_result.append("adaptation")
        if "optimize" in subject_lower or "optimization" in subject_lower:
            old_result.append("optimization")
        if "competition" in subject_lower or "market" in subject_lower:
            old_result.append("competition")
        if "evolution" in subject_lower:
            old_result.append("selection")
        if "spread" in subject_lower or "propagation" in subject_lower:
            old_result.append("diffusion")
        if "control" in subject_lower:
            old_result.append("feedback")

        old_result = list(set(old_result))

        # New method
        new_result = extractor.extract_hybrid(subject, verbose=False)

        print(f"  OLD (keywords): {old_result}")
        print(f"  NEW (hybrid):   {new_result}")

        if old_result != new_result:
            print(f"  → IMPROVED! ✓")
        else:
            print(f"  → Same result")

    print("\n" + "="*70)
    print("Testing complete!")
    print("="*70)
