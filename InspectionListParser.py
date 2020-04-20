from urllib.parse import urlparse, parse_qs, urljoin
from urllib.request import urlopen

from bs4 import BeautifulSoup

from Inspection import Inspection
from InspectionReportParser import get_inspection_type_and_violations
from ParseException import ParseException


# filter href which contain report url
def filter_reports_anchor(href: str):
    return href and href.__contains__("report_full.cfm")


# find all url of reports in the document
def get_inspection_anchors(document: BeautifulSoup):
    return document.find_all(href=filter_reports_anchor)


# get all divs (parent of url sections)
def get_inspection_divs(document: BeautifulSoup):
    anchors = get_inspection_anchors(document)
    divs = []
    for a in anchors:
        divs.append(a.parent)
    return divs


##################
def parse_report_url(element):
    return element.a["href"]


def parse_id(url):
    if not url:
        raise ParseException()
    url = urlparse(url)
    dictionary = parse_qs(url.query)
    if "inspectionID" not in dictionary:
        raise ParseException()
    ids = dictionary["inspectionID"]
    if len(ids) != 1:
        raise ParseException()
    return ids[0]


def parse_grade_and_date(element):
    inspection_div_strings = element.stripped_strings
    next(inspection_div_strings)
    inspection_date = next(inspection_div_strings)
    next(inspection_div_strings)
    inspection_grade = next(inspection_div_strings)
    return inspection_grade, inspection_date


def parse_types_and_violations(url):
    return get_inspection_type_and_violations(url)


def build_report_url(report_url_relative):
    return urljoin("https://ca.healthinspections.us/napa", report_url_relative.replace(" ", "%20"))


def parse_inspection_report(div):
    report_url_relative = parse_report_url(div)
    inspection_id = parse_id(report_url_relative)
    grade, date = parse_grade_and_date(div)
    report_url = build_report_url(report_url_relative)
    type, violations = parse_types_and_violations(report_url)
    return Inspection(inspection_id, type, grade, date, violations)


def get_inspection_list_document_url(permit_id):
    return "https://ca.healthinspections.us/napa/estab.cfm?permitID=" + permit_id


def get_inspection_list_document(permit_id):
    url = get_inspection_list_document_url(permit_id)
    url_data = urlopen(url)
    html_content = url_data.read()
    return BeautifulSoup(html_content, "lxml")


def parse_inspection_reports(permit_id):
    inspection_list_document = get_inspection_list_document(permit_id)
    inspection_divs = get_inspection_divs(inspection_list_document)
    inspections = []
    for div in inspection_divs:
        inspection = parse_inspection_report(div)
        inspections.append(inspection)
    return inspections
