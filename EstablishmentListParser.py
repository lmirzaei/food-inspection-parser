from Establishment import Establishment
from ParseException import ParseException
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


def get_establishment_divs(soup: BeautifulSoup):
    anchors = get_establishment_anchors(soup)
    divs = []
    for a in anchors:
        divs.append(a.parent)
    return divs


# To filter: define a function that takes an element as its only argument. The function should return True if the argument matches, and False otherwise.
# If you pass in a function to filter on a specific attribute like href, the argument passed into the function will be the attribute value, not the whole tag.
# Here’s a function that finds all a tags whose href attribute match a regular expression  :  estab.cfm?permitID=
def filter_estab(href: str):
    return href and href.startswith("estab.cfm?permitID")


def get_establishment_anchors(soup: BeautifulSoup):
    return soup.find_all(href=filter_estab)  # return an iterable type


# Create an establishment object via parsing an establishment's div
def parse_id(element):
    href_value = element.a["href"]
    # create a funtion that gets a string and return an id
    return get_id_from_string(href_value)


def get_id_from_string(href_value):
    if not href_value:
        raise ParseException()
    url = urlparse(href_value)
    dictionary = parse_qs(url.query)
    if "permitID" not in dictionary:
        raise ParseException()
    ids = dictionary["permitID"]
    if len(ids) != 1:
        raise ParseException()
    return ids[0]


def parse_name(element):
    return element.a.string


def parse_address(element):
    address_div_strings = get_address_strings(element)
    address = next(address_div_strings)
    return address


def parse_city_state_zipcode(element):
    city_state_zipcode_strings = get_address_strings(element)
    next(city_state_zipcode_strings)
    city_state_zipcode = next(city_state_zipcode_strings)
    return extract_city_state_zipcode(city_state_zipcode)


def get_address_strings(element):
    return element.find_all("div")[1].stripped_strings


def extract_city_state_zipcode(string):
    match = re.search(r"(.*), (\w{2}) ([0-9]{5})", string)
    return match.group(1), match.group(2), int(match.group(3))


def parse_establishment_div(element):
    permit_id = parse_id(element)
    name = parse_name(element)
    address = parse_address(element)
    city, state, zipcode = parse_city_state_zipcode(element)

    return Establishment(permit_id, name, address, city, state, zipcode)
