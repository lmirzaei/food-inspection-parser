# Create a class for violation
# each violation requires to have these variables: Number, Description


class Violation:
    def __init__(self, violation_number: str, description: str):
        self.violation_number = violation_number
        self.description = description

    def __str__(self):
        return "Number: " + self.violation_number + "\n\t\tDescription: " + self.description
