"""
This module contains various functions that can be used to convert, 
analyze and extract text from a pdf focument.

This module assumes the use of a weighbridge ticket, 
and an optional invoice.

The goal is to keep all logic used in this app isolated in this module,
and to have a dictionray of data point safter its use
"""
import re as regex
from pdf2image import convert_from_bytes
import pytesseract




def convert_pdf_to_image(pdf, output_location, filename, filetype):
    """
    Take a given pdf file
    And convert it to image files using
    the given constraints.
    """

    convert_from_bytes(
        open(pdf, 'rb').read(),
        output_folder=output_location,
        fmt=filetype,
        first_page=1,
        last_page=2,
        output_file=filename)

    filenames = [f"{output_location}/{filename}0001-1.{filetype}",
                f"{output_location}/{filename}0001-2.{filetype}"]

    print(f"{pdf} has been converted into images {filenames[0]} and {filenames[1]}")
    return filenames



def extract_text(filename):
    """
    Extract and return the raw text on an image
    """
    raw_text = pytesseract.image_to_string(filename)
    if isinstance(raw_text, str):
        return raw_text
    return "ERROR: no text was extracted from the proveided image"



def filter_text(page1, page2, user):
    """
    Filter raw text and return a dictionary containing
    the neccessary data points
    """
    # Identify page data
    if page2 != "None":
        ticket = page2
        invoice = page1
    else:
        ticket = page1
        invoice = 0

    # build a data dictionary to contain all data points
    data = {}

    ## Data points
    # Scale clerk
    data.update({"clerk": f"{user}"})

    # Weighbridge number
    wb_pattern = r'WB\d+'
    data.update({"wb": f"{regex.findall(wb_pattern, ticket)}"})

    # Contract number
    sor_pattern = r'SOR00\d+'
    data.update({"sor": f"{regex.findall(sor_pattern, ticket)}"})

    # Invoice number
    psi_pattern = r'PS\d+'
    if invoice:
        invoice = regex.findall(psi_pattern, invoice)
        if invoice[0].find("PS1") != -1:
            invoice[0] = invoice[0].replace("1", "I", 1) #  Tesseract reads PS1 instead of PSI, so we fix it here
 
        data.update({"psi": invoice})
    else:
        data.update({"psi": "None"})

    # Time in and out
    time_pattern = r'\d{2}:\d{2}:\d{2}'
    times = regex.findall(time_pattern, ticket)
    time_in_values = times[::2]
    time_out_values = times[1::2]
    for time_in, time_out in zip(time_in_values, time_out_values):
        #print(f"Time In: {time_in}, Time Out: {time_out}")
        data.update({"time_in": time_in})
        data.update({"time_out": time_out})

    # Net Weight
    weight_pattern = r'\b\d{1,2},\d{3}\b'
    weight_values = regex.findall(weight_pattern, ticket,)
    weight_values = [int(value.replace(",", "")) for value in weight_values]
    data.update({"net_weight": weight_values[0]})

    # Product
    PRODUCTS = [
        "SOYBEAN OIL DEGUMMED",
        "SOYBEAN OIL NON DEGUMMED"
        "SOYBEAN OIL GUMS",
        "SOYA HULLS",
        "SOYBEAN OIL SLUDGE",
        "COAL",
        "HEXANE",
        "SOYBEAN OILCAKE",
        "SOYBEAN OILCAKE 50kg WIP",
        "SOYBEAN WHITE FLAKES",
        "SOYBEAN WHITE FLAKES 50kg WIP",
        "ASH COLECTION"
    ]

    for item in PRODUCTS:
        if ticket.find(item) != -1:
            product_return = item.replace("SOYBEAN", "")
            break

    data.update({"product": product_return})

    # Client
    lines = ticket.split("\n")

    for idx, line in enumerate(lines):
        if "Customer/Vendor" in line:
            if idx+ 1 < len(lines):
                extract = lines[idx+1].strip()
                customer_name = extract.replace("Vehicle Reg. Driver ID & Name", "")
                data.update({"customer": customer_name})

    # Transporter
    for idx, line in enumerate(lines):
        if "Nett Weight" in line:
            if idx+ 1 < len(lines):
                extract = lines[idx+1].strip()
                transporter = extract.replace("Transporter: ", "")
                data.update({"transporter": transporter})

    # Store
    if ticket.find("VKB STORE") != -1 or ticket.find("SHUTTLE") != -1:
        data.update({"store": "vkb store"})
        data.update({"type": "ext"})
    else:
        data.update({"store": "plant"})
        data.update({"type": "None"})

    # Type
    if data["type"] != "ext":
        if ticket.find("INCOMING") != -1:
            data.update({"type": "in"})
        else:
            data.update({"type": "out"})

    return data



def analyze(pdf, user):
    """
    This function combines the three previous functions into a single function.
    It will take care of specifications, conditionals and exceptions,
    allowing for a simple application of the function within the main.py app module.
    """

    # convert pdf to images
    filenames = convert_pdf_to_image(pdf, "app/output", "page", "jpg")
    print(filenames)

    contents = []
    # extract text from images
    contents.append(extract_text(filenames[0]))
    # check if page1 is an invoice and convert second page to text if true
    if contents[0].find("Tax Invoice") != -1:
        contents.append(extract_text(filenames[1]))
    else:
        contents.append("None")

    # filter text
    data = filter_text(contents[0], contents[1], user)

    return data


# Test section
print(analyze("app/docs/1.pdf", "Arnold"))

# TODO: Implement proper exception handling into functions
# TODO: test difference in results between internal and warehouse release tickets. Make changes as needed
