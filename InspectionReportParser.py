from urllib.request import urlopen

from bs4 import BeautifulSoup

from ParseException import ParseException
from Violation import Violation


def get_inspection_type_and_violations(report_url: str):
    url_data = urlopen(report_url)
    html_content = url_data.read()
    report_document = BeautifulSoup(html_content, "lxml")
    inspection_type = get_inspection_type(report_document)
    violations = get_violations(report_document)
    return inspection_type, violations


def get_inspection_type(report_document):
    if not report_document:
        raise ParseException()
    divs = report_document.find_all(class_="topSection")
    if not divs:
        raise ParseException()
    top_section_div = divs[0]
    return list(top_section_div.stripped_strings)[-1]


def get_violations(report_document):
    if not report_document:
        raise ParseException()
    report_tables = report_document.find_all(class_="insideTable")
    if not report_tables:
        raise ParseException()
    violations = []
    # There are two tables in the report HTML, one for each side.
    for t in report_tables:
        report_rows = t.find_all("tr", class_=False)
        if not report_rows:
            raise ParseException()
        violations += create_violations(report_rows)

    return violations


def create_violations(report_rows):
    violations = []
    for row in report_rows:
        # get all columns for a row
        violation = create_violation(row, violations)
        if violation:
            violations.append(violation)
    return violations


def create_violation(row, violations):
    row_columns = row.find_all("td")
    out_of_compliance_image = row_columns[2].img["src"]
    if "box_checked" in out_of_compliance_image:
        first_columns_text = row_columns[0].string
        first_columns_text_parts = first_columns_text.partition(".")
        violation_item_number = first_columns_text_parts[0]
        description = first_columns_text_parts[2].strip()
        return Violation(violation_item_number, description)
    else:
        return None
