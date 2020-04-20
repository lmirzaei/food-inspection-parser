# Create a class for inspection
# each inspection requires to have these variables: ID, Type, Grade, Date
# each inspection should have a list for all violations
from Violation import Violation


class Inspection:
    def __init__(self, inspection_id: str, inspection_type: str, grade: str, date: str, violations: [Violation]):
        self.inspection_id = inspection_id
        self.inspection_type = inspection_type
        self.grade = grade
        self.date = date
        self.violations = violations

    def __str__(self):
        violations_str = ""
        for violation in self.violations:
            violations_str += "\t\t" + violation.__str__() + "\n"
        return "Inspection ID: " + self.inspection_id + "\n\tInspection Type: " + self.inspection_type + "\n\tGrade: " + self.grade + "\n\tDate: " + self.date + "\n\tViolations:\n" + violations_str
