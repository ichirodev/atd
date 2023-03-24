from flask import jsonify

class MedicamentPackage:
    def __init__(self, name, concentration, route_of_administration, purpose):
        self.name = name
        self.concentrarion = concentration
        self.route_of_administration = route_of_administration
        self.purpose = purpose

    def json(self):
        return jsonify(
            name = self.name,
            concentration = self.concentrarion,
            route_of_administration = self.route_of_administration,
            purpose = self.purpose
        )