import imagehash
from PIL import Image


class CardModul:
    """卡类型模型"""
    temple_card = [
        {"phash": imagehash.average_hash(Image.open(
            'img/ff0f0f3f1f030707.jpeg')), "typeId": 1, "name": "商旅管家随行礼品卡", "cut": (130, 1340, 1047, 1496)},
        {"phash": imagehash.average_hash(Image.open(
            'img/ffe20080fee0c3c1.jpeg')), "typeId": 2, "name": "商旅管家(黑)", "cut": (160, 1070, 2270, 1288)},
        {"phash": imagehash.average_hash(Image.open(
            'img/ff8dc7808081c1c1.jpeg')), "typeId": 3, "name": "商旅管家(金)", "cut": (160, 1070, 2290, 1372)},
    ]

    def compare(self, traget_phash):
        index_phash = 100
        card = {}
        for i in self.temple_card:
            # 计算汉明距离
            hamming_distance = traget_phash - i["phash"]
            if hamming_distance < 30:
                if index_phash > hamming_distance:
                    index_phash = hamming_distance
                    card = i
        return card
