from PIL import Image

# pdf2image
from pdf2image import convert_from_bytes

# pytesseract
import pytesseract


# Simple image to string
print(pytesseract.image_to_string(Image.open('test.png')))


# Convert pdf to image
filename = "f"

images = convert_from_bytes(
    open('dummy.pdf', 'rb').read(),
    output_folder='output',
    fmt='jpeg',
    first_page=1,
    last_page=2,
    output_file=filename)

print(pytesseract.image_to_string(f'output/{filename}0001-1.jpg'))
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print(pytesseract.image_to_string(f'output/{filename}0001-2.jpg'))
