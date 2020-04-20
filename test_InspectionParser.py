from unittest import TestCase

from bs4 import BeautifulSoup

import InspectionListParser


def load_test_document():
    with open("inspections1313MainSt.htm") as fp:
        return BeautifulSoup(fp)


class TestFilterReportsAnchor(TestCase):
    def test_filter_reports_anchor_succeed(self):
        actual = InspectionListParser.filter_reports_anchor(
            "https://ca.healthinspections.us/_templates/135/Food%20Inspection/_report_full.cfm?domainID=135&inspectionID=313513&dsn=dhd_135")
        self.assertTrue(actual)

    def test_filter_reports_anchor_fail(self):
        actual = InspectionListParser.filter_reports_anchor(
            "https://ca.healthinspections.us/_templates/135/Food%20Inspection/")
        self.assertFalse(actual)


class TestGetInspectionAnchors(TestCase):
    def test_get_inspection_anchors(self):
        document = load_test_document()
        anchors_iterable = InspectionListParser.get_inspection_anchors(document)
        actual = list(anchors_iterable)
        self.assertEqual(len(actual), 9)

        for link in actual:
            self.assertEqual(link.name, "a")
            self.assertTrue(link["href"].__contains__("report_full.cfm"))


class TestGetInspectionDivs(TestCase):
    def test_get_inspection_divs(self):
        document = load_test_document()
        divs_iterable = InspectionListParser.get_inspection_divs(document)
        actual = list(divs_iterable)
        self.assertEqual(len(actual), 9)

        for tag in actual:
            self.assertEqual(tag.name, "div")
