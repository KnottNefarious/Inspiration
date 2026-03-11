import re

MECHANISM_WORDS = [

"diffusion",
"competition",
"selection",
"optimization",
"feedback",
"oscillation",
"propagation",
"synchronization",
"adaptation",
"evolution",
"stochastic",
"dynamical"

]


def extract_mechanisms_from_text(text):

    found = []

    text = text.lower()

    for m in MECHANISM_WORDS:

        if re.search(rf"\b{m}\b", text):

            found.append(m)

    return list(set(found))
