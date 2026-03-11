import json
from system_model import System

DATABASE_FILE = "data/learned_systems.json"


def load_systems():

    try:

        with open(DATABASE_FILE) as f:

            data = json.load(f)

        return [System.from_dict(x) for x in data]

    except:

        return []


def save_systems(systems):

    with open(DATABASE_FILE, "w") as f:

        json.dump([s.to_dict() for s in systems], f, indent=2)
