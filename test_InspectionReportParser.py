from unittest import TestCase

from bs4 import BeautifulSoup

import InspectionReportParser


def load_test_document():
    with open("FoodFacilityInspectionReport.htm") as fp:
        return BeautifulSoup(fp)


class TestGetInspectionType(TestCase):
    def test_get_inspection_type(self):
        report_document = load_test_document()
        actual = InspectionReportParser.get_inspection_type(report_document)
        self.assertEqual(actual, "Routine")
