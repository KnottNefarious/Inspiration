class System:

    def __init__(self, name, domain, structures, mechanisms, math_models):

        self.name = name
        self.domain = domain
        self.structures = structures
        self.mechanisms = mechanisms
        self.math_models = math_models

    def to_dict(self):

        return {
            "name": self.name,
            "domain": self.domain,
            "structures": self.structures,
            "mechanisms": self.mechanisms,
            "math_models": self.math_models
        }

    @staticmethod
    def from_dict(data):

        return System(
            data["name"],
            data["domain"],
            data["structures"],
            data["mechanisms"],
            data["math_models"]
        )
