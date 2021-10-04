import xml.etree.ElementTree as ET
import argparse
import os


class ParcelInfo:
    """Represents a piece of information to be retrieved from the input file"""

    missing_text = 'Brak'  # String to display if the value isn't found

    def __init__(self, display_name, *args):
        self.display_name = display_name  # Printed as a label for the information
        # Initialize a dictionary where each valid data format maps to a tag name
        self.format_tags = {key: str(tag) for (key, tag) in zip(valid_formats, args)}
        self.value = None

    def show(self):
        """Prints a representation of the information"""
        print(f"{self.display_name}: {self.value or self.missing_text}")

    def load_from_data(self, file_format, data_format, data):
        """Changes the 'value' field of this object by retrieving data from a file"""
        new_value = None
        if data_format not in self.format_tags or not data:
            new_value = None  # None if the correct tag name isn't stored in the object
        if file_format == '.xml':
            new_value = self.get_xml_tag(data_format, data)
        self.value = new_value

    def get_xml_tag(self, data_format, data):
        """Returns the content of the proper tag from a parsed xml file"""
        tag_name = self.format_tags[data_format]  # Get tag name based on data format
        tag = data.find('.//{*}' + tag_name)  # Search for the tag ignoring namespaces
        return tag.text if tag is not None else None


# Valid data formats used as arguments for the program
valid_formats = ['nas', 'aaa']

# Initialize all required pieces of information as ParcelInfo objects.
# The first argument is the label for display.
# The following arguments should map to the array of valid formats as tags or keys used to retrieve the information.
info = [
    ParcelInfo('Numer działki', 'flurstueckskennzeichen', 'flstkennz'),
    ParcelInfo('Wielkość działki', 'amtlicheFlaeche', 'flaeche'),
    ParcelInfo('Numer landu', 'land', 'landschl'),
    ParcelInfo('Numer okręgu', 'kreis', 'kreisschl'),
    ParcelInfo('Numer powiatu', 'gemeinde', 'gmdschl'),
    ParcelInfo('Numer gemarkung', 'gemarkungsnummer', 'gemaschl'),
]


def main(data_format, file):
    file_format = os.path.splitext(file)[1]
    data = parse_file(file_format, file)
    for i in info:
        i.load_from_data(file_format, data_format, data)
        i.show()


def parse_file(file_format, file):
    """Parses the file before it's searched for information. Perform actions that should be done only once here"""
    if file_format == '.xml':
        return ET.parse(file)
    else:
        raise Exception("Wrong file format.")


def parse_arguments():
    parser = argparse.ArgumentParser(description='Prints information about a parcel')
    parser.add_argument('data_format', help='data format used in the target file', choices=valid_formats)
    parser.add_argument('file', help='name of file containing the information')
    arguments_namespace = parser.parse_args()
    return vars(arguments_namespace)


if __name__ == '__main__':
    arguments = parse_arguments()
    main(**arguments)
