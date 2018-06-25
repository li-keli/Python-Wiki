from PIL import Image
from PIL import ImageDraw
from PIL import ImageOps
from io import BytesIO
from pyocr import tesseract
from card_type import *
import imagehash
import os


def get_text(img_byte, card_modul):
    """识别卡号"""
    im = Image.open(BytesIO(img_byte))
    
    if card_modul['typeId'] == 1:
        # 剪裁
        region = im.crop(card_modul["cut"])
    elif card_modul['typeId'] == 2:
        # 剪裁
        region = im.crop(card_modul["cut"])
    elif card_modul['typeId'] == 3:
        # 剪裁
        region = im.crop(card_modul["cut"])

    region = ImageOps.invert(region).convert("L")
    region.show()

    # OCR
    builder = tesseract.builders.DigitBuilder()
    digits_address = os.path.join(os.getcwd(), 'config/digits')
    builder.tesseract_configs = ['-psm', '7', digits_address]
    result = tesseract.image_to_string(region, 'eng', builder)
    return result.replace(' ', '')

def recognition_card_type(img_byte):
    """识别卡类型"""
    im = Image.open(BytesIO(img_byte))
    new_phash = imagehash.average_hash(im)
    print(new_phash)
    return CardModul().compare(new_phash)

