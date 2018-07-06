from PIL import Image
from PIL import ImageDraw
from PIL import ImageOps
from io import BytesIO
from pyocr import tesseract
from card_type import *
import imagehash
import os


im = Image.open("img/ff8dc7808081c1c1.jpeg")
im = im.crop((160, 1070, 2290, 1372))
old_width, old_height = im.size
im.thumbnail((old_width*0.2, old_height*0.2))
im = ImageOps.invert(im).convert("L")

builder = tesseract.builders.DigitBuilder()
digits_address = os.path.join(os.getcwd(), 'config/digits')
builder.tesseract_configs = ['-psm', '7', digits_address]
result = tesseract.image_to_string(im, 'eng', builder)

im.show()
print(result.replace(" ", ""))