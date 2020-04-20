import json
from urllib.request import urlopen

from bs4 import BeautifulSoup

import EstablishmentListParser
import InspectionListParser
from EstablishmentEncoder import EstablishmentEncoder


def parse_inspections(link):
    url_data = urlopen(link)
    html_content = url_data.read()
    document = BeautifulSoup(html_content, "lxml")
    divs = EstablishmentListParser.get_establishment_divs(document)
    establishments = []
    for establishment_div in divs:
        establishment = EstablishmentListParser.parse_establishment_div(establishment_div)
        inspections = InspectionListParser.parse_inspection_reports(establishment.permit_id)
        establishment.inspections = inspections
        establishments.append(establishment)
        print(establishment)

    with open("food_inspection_report.json", "w") as json_file:
        json.dump(establishments, json_file, indent=2, cls=EstablishmentEncoder)


def main():
    url = "https://ca.healthinspections.us/napa/search.cfm?start=1&1=1&sd=01/01/1970&ed=03/01/2017&kw1=&kw2=&kw3=&rel1=N.permitName&rel2=N.permitName&rel3=N.permitName&zc=&dtRng=YES&pre=similar"
    parse_inspections(url)


if __name__ == '__main__':
    main()
