import unittest
import xml.etree.ElementTree as ET

from solution_jgadek import ParcelInfo, valid_formats, parse_file

nas_file = 'parcel_nas.xml'
aaa_file = 'parcel_aaa.xml'


class TestParcelInfo(unittest.TestCase):
    def test_init(self):
        # Test correct mapping of arguments to data types
        info = ParcelInfo("Test", 'tag1')
        assert len(info.format_tags) == 1
        assert info.format_tags[valid_formats[0]] == 'tag1'

        # Assert that the dictionary maps correctly even with too many arguments
        info = ParcelInfo("Test", 'tag1', 'tag2', 'tag3')
        assert len(info.format_tags) == 2

    def test_get_xml_tag(self):
        data = ET.parse(nas_file)

        # Test that the correct tag content is return with proper configuration
        info = ParcelInfo('Test', 'flurstueckskennzeichen')
        assert info.get_xml_tag('nas', data) == '095653___05443______'

        # Assert that None is returned when the tag name is wrong
        info = ParcelInfo('Test', 'nonexistenttag')
        assert info.get_xml_tag('nas', data) is None

    def test_load_from_data(self):
        # Test correct retrieval of data in aaa format with proper configuration
        data = ET.parse(aaa_file)
        info = ParcelInfo('Test', 'tag1', 'kreisschl')
        info.load_from_data('.xml', 'aaa', data)
        assert info.value == '05378'

        # Test correct retrieval of data in nas format with proper configuration
        data = ET.parse(nas_file)
        info = ParcelInfo('Test', 'flurstueckskennzeichen', 3)
        info.load_from_data('.xml', 'nas', data)
        assert info.value == '095653___05443______'

        # Assert the value is overwritten with None when wrong file format is passed
        info.load_from_data('.xyz', 'aaa', data)
        assert info.value is None

        # Assert the value is overwritten with None when wrong file format is passed
        info.load_from_data('.xml', 'nas', data)
        info.load_from_data('.xml', 'aaa', data)
        assert info.value is None

        # Assert the value is overwritten with None when wrong file format is passed
        info = ParcelInfo("Test", 'flurstueckskennzeichen')
        info.load_from_data('.xml', 'nas', data)
        info.load_from_data('.xyz', 'nas', data)
        assert info.value is None


class TestMain(unittest.TestCase):
    def test_parse_file(self):
        # Assert that parse_file returns an instance of ElementTree when used with an xml file
        assert isinstance(parse_file('.xml', nas_file), ET.ElementTree)
        # Assert that using a wrong file format raises an exception
        self.assertRaises(Exception, parse_file, '.xyz', nas_file)


if __name__ == '__main__':
    unittest.main()
