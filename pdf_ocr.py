"""
This module contains various functions that can be used to convert, 
analyze and extract text from a pdf focument.

This module assumes the use of a weighbridge ticket, 
and an optional invoice.

The goal is to keep all logic used in this app isolated in this module.
"""

from pdf2image import convert_from_bytes
import pytesseract



def convert_pdf_to_image(pdf, output_location, filename):
    """
    Take a given pdf file
    And convert it to image files using
    the given constraints.
    """
    convert_from_bytes(
        open(pdf, 'rb').read(),
        output_folder=output_location,
        fmt='jpeg',
        first_page=1,
        last_page=2,
        output_file=filename)
    return


def extract_text(filename):
    """
    Extract and return the raw text on an image
    """
    raw_text = pytesseract.image_to_string(filename)
    if raw_text:
        return raw_text
    return "ERROR: no text was extracted from the proveided image"


def filter_text():
    """
    Filter raw text and return a dictionary containing
    the neccessary data points
    """
    return # TODO


# TODO: Implement proper exception handling into functions
