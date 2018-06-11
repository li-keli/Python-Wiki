import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageOps
from io import BytesIO
from pyocr import tesseract
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


def down_img():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36",
        "Host": "www.hqew.com",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    }
    for _ in range(1, 2):
        img = requests.get(
            'http://www.hqew.com/robottocheck/image', headers=headers).content
        get_text(img)


def get_text(img_byte):
    im = Image.open(BytesIO(img_byte))
    # 去底色
    im = im.point(lambda i: 255 if i > 150 else 0)

    # 去除干扰线
    size = im.size
    pimx = im.load()
    for x in range(size[0]):
        for y in range(size[1]):
            px = pimx[x, y]
            if px[0] == 0 and px[1] == 0 and px[2] == 0:
                pimx[x, y] = (255, 255, 255)
    im = im.convert("L")
    # im = ImageOps.invert(im).convert("1")
    # old_width, old_height = im.size
    # im.thumbnail((old_width*0.7, old_height*0.7))

    arr = np.array(im).sum(axis=0)
    print(arr)

    # 剪裁
    region = im.crop((36, 1, 105, 34))
    # region.show()

    # OCR
    builder = tesseract.builders.TextBuilder()
    builder.tesseract_configs = ['-psm', '7', './digits']
    result = tesseract.image_to_string(region, 'eng', builder)

    if len(result.replace(' ', '')) == 4:
        region.save("img/%s.jpg" % result)


if __name__ == "__main__":
    down_img()
