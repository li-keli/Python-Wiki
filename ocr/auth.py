import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageOps
from io import BytesIO
from pyocr import tesseract
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

"""
华强电子 验证码识别
侵权删
"""


def down_img():
    """下载验证码"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36",
        "Host": "www.hqew.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    }
    for _ in range(1, 10):
        img = requests.get(
            'http://www.hqew.com/robottocheck/image', headers=headers).content
        get_text(img)


def get_text(img_byte):
    """识别"""
    im = Image.open(BytesIO(img_byte))
    # 去底色
    im = im.point(lambda i: 255 if i > 180 else 0)

    # 去除干扰线
    size = im.size
    pimx = im.load()
    for x in range(size[0]):
        for y in range(size[1]):
            px = pimx[x, y]
            if px[0] == 0 and px[1] == 0 and px[2] == 0:
                pimx[x, y] = pimx[x, 0 if y == 0 else y - 1]

    im = ImageOps.invert(im).convert("1")
    old_width, old_height = im.size
    im.thumbnail((old_width*0.7, old_height*0.7))

    arr = np.array(im).sum(axis=0)
    print(arr)

    # 剪裁
    region = im.crop((36, 1, 105, 34))

    # OCR
    builder = tesseract.builders.DigitBuilder()
    digits_address = os.path.join(os.getcwd(), 'config/digits')
    print("digits_address -> ", digits_address)
    builder.tesseract_configs = ['-psm', '7', digits_address]
    result = tesseract.image_to_string(region, 'eng', builder)

    code_text = result.replace(' ', '')
    print("out text -> ", code_text)
    if len(code_text) == 4:
        return str(code_text)
    else:
        return "0"
