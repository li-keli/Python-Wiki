from urllib import parse
import pandas as pd
import hashlib
import time
import requests
import json

"""
1. 根据csv列表数据查询所有去哪儿的酒店房型
2. 取出某家酒店中7月15日价格最低的前三个房型
3. 导出csv
"""


def do_md5(info):
    return hashlib.md5(info.encode(encoding='utf-8')).hexdigest()


def get_quner(hotel_code):
    url = 'http://api.hds.qunar.com/api/hotel/queryRatePlan.json?reqData='
    request_data = {
        "head": {
            "appKey": "10655351",
            "salt": str(int(time.time())),
            "version": "3.1.0",
            "sign": do_md5(do_md5('BPTLxWMl' + '10655351') + str(int(time.time())))
        },
        "data": {
            "arrivalDate": "2018-07-15",
            "departureDate": "2018-07-16",
            "hotelIds": hotel_code,
            "isSkipHdsCondition": "false"
        }
    }
    response_json = requests.get(url + parse.quote(json.dumps(request_data))).json()
    if response_json['code'] == 0:
        return True, response_json['result'],
    else:
        return False, response_json['errMsg']


if __name__ == '__main__':
    target_data = []

    data_source = pd.DataFrame(pd.read_csv("./产品部-1080-对应去哪酒店数据769.csv", header=1, encoding='utf-8', engine='python'))
    for indexs in data_source.index:
        hotelcode = data_source.loc[indexs].values[1]
        hotelname = data_source.loc[indexs].values[0]
        print(hotelcode, hotelname)

        isOk, hotels = get_quner(hotelcode)
        if isOk:
            for hotel in hotels['hotels']:

                min_limit = []

                for room in hotel['rooms']:
                    min_price = 999999
                    min_product_room_name = ''

                    for ratePlan in room['ratePlans']:
                        for nightlyRate in ratePlan['nightlyRates']:
                            if nightlyRate['cost'] != 1 and nightlyRate['status'] == True:
                                if nightlyRate['cost'] < min_price:
                                    min_price = round(nightlyRate['cost'] * 1.06, 2)
                                    min_product_room_name = ratePlan['productRoomName'].replace(room['name'], '')
                    min_limit.append([hotelname, room['name'], min_product_room_name, min_price])
                min_limit.sort(key=lambda elem: elem[3])
                target_data.extend(min_limit[:3])
    pd.DataFrame(target_data, columns=('酒店名称', '房型名称', 'RP名称', '房型最低价')).to_csv("test.csv", encoding='utf-8', index=False)
