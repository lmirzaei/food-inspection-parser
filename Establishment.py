# Create a class for establishment
# each establishment require to have these variables: ID, Name, Address, City, State, Zipcode
# each establishment should have a list for all inspections
# this class needs a function to add a new inspection
class Establishment:
    def __init__(self, permit_id: str, name: str, address: str, city: str, state: str, zipcode: int):
        self.permit_id = permit_id
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.inspections = []

    def __str__(self):
        inspections_str = ""
        for inspection in self.inspections:
            inspections_str += "\t" + inspection.__str__() + "\n"

        return "Permit ID: " + self.permit_id + "\nName: " + self.name + "\nAddress: " + self.address + "\nCity: " + self.city + "\nState: " + self.state + "\nZip code: " + str(
            self.zipcode) + "\nInspections:\n" + inspections_str
