import re
import pypdfium2 as pdfium

# This function reads the file data/FS-Rules_2024_v1.1.0.txt and extracts the titles and texts of the rules.

# For example, the file contains the following text:
# """
#    AIP
#
# Anti Intrusion Plate
# """
#
# or in this format:
# """
# A 1.2.6
# 
# Vehicles of both classes can take part in an additional Driverless Cup (DC).
# """
#
# arguments:
# file_name: str: the file name of the rules in .pdf format
def extract_rules_from_pdf(file_name='data/Rules_2024_v1.1.pdf'):

    pdf = pdfium.PdfDocument(file_name)

    full_text = ""

    for page in pdf:
        textpage = page.get_textpage()
        full_text += textpage.get_text_range()
        # print(full_text)

    # Split the text into lines
    lines = full_text.split("\n")

    # Initialize variables
    pattern = re.compile(r'^[A-Z]+\d+\.\d+\.\d+')
    current_rule = None
    rules_splitted = []

    # Iterate through the lines and group them based on the rule identifiers
    for line in lines:
        if pattern.match(line):
            current_rule = line.strip()
            rules_splitted.append(current_rule)
        elif current_rule:
            rules_splitted[-1] += "\n" + line.strip()
            
    return rules_splitted