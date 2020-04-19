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

    def __str__(self):
        return "Permit ID: " + self.permit_id + " Name: " + self.name + " Address: " + self.address + " City: " + self.city + " State: " + self.state + " Zip code: " + str(
            self.zipcode)
