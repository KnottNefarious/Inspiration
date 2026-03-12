MECHANISM_GRAPH = {

"diffusion": {
"math": "PDE",
"equation": "diffusion",
"algorithm": "graph diffusion",
"weight": 5
},

"optimization": {
"math": "calculus",
"equation": "gradient",
"algorithm": "gradient descent",
"weight": 5
},

"selection": {
"math": "dynamical systems",
"equation": "replicator",
"algorithm": "evolutionary search",
"weight": 4
},

"competition": {
"math": "game theory",
"equation": "replicator",
"algorithm": "equilibrium solver",
"weight": 3
},

"feedback": {
"math": "control theory",
"equation": "linear control",
"algorithm": "control loop",
"weight": 3
},

"oscillation": {
"math": "wave dynamics",
"equation": "wave",
"algorithm": "signal propagation",
"weight": 4
},

"chaos": {
"math": "nonlinear dynamics",
"equation": "chaotic map",
"algorithm": "chaotic search",
"weight": 2
},

"congestion": {
"math": "network flow",
"equation": "flow equation",
"algorithm": "traffic optimization",
"weight": 1
}

}