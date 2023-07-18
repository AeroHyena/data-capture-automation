"""
This is a Python script built to explore text extraction from a pdf file.

This is done by converting the pdf file to images, 
and then using ocr technolies on the images to extract the text.
"""
from PIL import Image

# pdf2image
from pdf2image import convert_from_bytes

# pytesseract
import pytesseract




#### Read the text on an test.png and print it to console
print(pytesseract.image_to_string(Image.open('test.png')))

# Line to seperate file contents in console
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')


#### Convert pdf to image, and read its contents
OUTPUT_FILENAME = "f"

# Convert pdf to images.
# Images are saved in the output folder in jpeg format.
# Only the first two pages of the pdf is read.
images = convert_from_bytes(
    open('dummy.pdf', 'rb').read(),
    output_folder='output',
    fmt='jpeg',
    first_page=1,
    last_page=2,
    output_file=OUTPUT_FILENAME)
print("Converted dummy.pdf")

OUTPUT_FILENAME2 = "g"
images2 = convert_from_bytes(
    open('dummy(invoice).pdf', 'rb').read(),
    output_folder='output',
    fmt='jpeg',
    first_page=1,
    last_page=2,
    output_file=OUTPUT_FILENAME2)
print("Converted dummy(invoice).pdf")


# Read the image files in the output folder,
# and print the contents to console.

x = pytesseract.image_to_string(f'output/{OUTPUT_FILENAME}0001-1.jpg')
print(x)
print(type(x))
if x.find("Tax Invoice") != -1:
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(pytesseract.image_to_string(f'output/{OUTPUT_FILENAME}0001-2.jpg'))
    print("Invoice found")
else:
    print("No invoice found")


print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')


x = pytesseract.image_to_string(f'output/{OUTPUT_FILENAME2}0001-1.jpg')
print(x)
print(type(x))
if x.find("Tax Invoice") != -1:
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(pytesseract.image_to_string(f'output/{OUTPUT_FILENAME2}0001-2.jpg'))
    print("Invoice found")
else:
    print("No invoice found")
