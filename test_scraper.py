from bs4 import BeautifulSoup
from unittest import TestCase
from ParseException import ParseException
import EstablishmentListParser


def load_test_document():
    with open("NapaIndex.html") as fp:
        return BeautifulSoup(fp)


class TestFilterEstab(TestCase):
    def test_filter_estab_for_non_estab_fails(self):
        actual = EstablishmentListParser.filter_estab("search.cfm?")
        self.assertFalse(actual)

    def test_filter_estab_for_estab_succeeds(self):
        actual = EstablishmentListParser.filter_estab("estab.cfm?permitID=249688&amp;inspectionID=402660")
        self.assertTrue(actual)


class TestGetEstablishmentAnchors(TestCase):

    def test_get_establishment_anchors(self):
        document = load_test_document()
        establishment_anchors_iterable = EstablishmentListParser.get_establishment_anchors(document)
        actual = list(establishment_anchors_iterable)
        self.assertEqual(len(actual), 10)

        for link in actual:
            self.assertEqual(link.name, "a")
            self.assertTrue(link["href"].startswith("estab.cfm"))


class TestGetEstablishmentDivs(TestCase):

    def test_get_establishment_divs(self):
        document = load_test_document()
        actual = EstablishmentListParser.get_establishment_divs(document)
        self.assertEqual(len(actual), 10)

        for tag in actual:
            self.assertEqual(tag.name, "div")


class TestParseId(TestCase):
    def test_parse_id(self):
        document = load_test_document()
        divs = EstablishmentListParser.get_establishment_divs(document)
        self.assertGreater(len(divs), 0)
        actual = EstablishmentListParser.parse_id(divs[0])
        self.assertEqual(actual, "249688")


class TestGetIdFromString(TestCase):
    # input : none, input : empty string, input: string with two IDs, input: string without any id, input: url without query string, input: happy case :)
    def test_get_id_from_string_none_throws(self):
        input = None
        self.assertRaises(ParseException, EstablishmentListParser.get_id_from_string, input)

    def test_get_id_from_string_empty_throws(self):
        input = ""
        self.assertRaises(ParseException, EstablishmentListParser.get_id_from_string, input)

    def test_get_id_from_string_two_ids_throws(self):
        input = "estab.cfm?permitID=249688&amp;permitID=402660"
        self.assertRaises(ParseException, EstablishmentListParser.get_id_from_string, input)

    def test_get_id_from_string_no_ids_throws(self):
        input = "estab.cfm?inspectionID=249688&amp;inspectionID=402660"
        self.assertRaises(ParseException, EstablishmentListParser.get_id_from_string, input)

    def test_get_id_from_string_without_query_string_throws(self):
        input = "estab.cfm"
        self.assertRaises(ParseException, EstablishmentListParser.get_id_from_string, input)

    def test_get_id_from_string_succeeds(self):
        input = "estab.cfm?permitID=249688&amp;inspectionID=402660"
        actual = EstablishmentListParser.get_id_from_string(input)
        self.assertEqual(actual, "249688")


class TestParseName(TestCase):
    def test_parse_name(self):
        document = load_test_document()
        divs = EstablishmentListParser.get_establishment_divs(document)
        self.assertGreater(len(divs), 0)
        actual = EstablishmentListParser.parse_name(divs[0])
        self.assertNotEqual(actual, "")
        self.assertNotEqual(actual, None)
        self.assertEqual(actual, "AC FOOD & LIQUOR")


class TestParseAddress(TestCase):
    def test_parse_address(self):
        document = load_test_document()
        divs = EstablishmentListParser.get_establishment_divs(document)
        self.assertGreater(len(divs), 0)
        actual = EstablishmentListParser.parse_address(divs[0])
        self.assertNotEqual(actual, "")
        self.assertNotEqual(actual, None)
        self.assertEqual(actual, "3915  BROADWAY  ST")


class TestParseCityStateZipcode(TestCase):
    def test_parse_city_state_zipcode(self):
        document = load_test_document()
        divs = EstablishmentListParser.get_establishment_divs(document)
        self.assertGreater(len(divs), 0)
        actual_city, actual_state, actual_zipcode = EstablishmentListParser.parse_city_state_zipcode(divs[0])

        self.assertNotEqual(actual_city, "")
        self.assertNotEqual(actual_city, None)
        self.assertEqual(actual_city, "AMERICAN CANYON")

        self.assertNotEqual(actual_state, "")
        self.assertNotEqual(actual_state, None)
        self.assertEqual(actual_state, "CA")

        self.assertEqual(actual_zipcode, 94503)


class TestParseEstablishmentDiv(TestCase):
    def test_parse_establishment_div(self):
        document = load_test_document()
        divs = EstablishmentListParser.get_establishment_divs(document)
        self.assertGreater(len(divs), 0)
        element = divs[0]
        actual = EstablishmentListParser.parse_establishment_div(element)
        self.assertEqual(actual.permit_id, "249688")
        self.assertEqual(actual.name, "AC FOOD & LIQUOR")
        self.assertEqual(actual.address, "3915  BROADWAY  ST")
        self.assertEqual(actual.city, "AMERICAN CANYON")
        self.assertEqual(actual.state, "CA")
        self.assertEqual(actual.zipcode, 94503)
