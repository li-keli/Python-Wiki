from urllib import parse
import requests
import pandas as pd

header = {
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'host': 'www.928383.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'cookie': 'QN1="O5cv5ls+3Zamu6FeB12KAg=="; QN219=540fd108-5da1-4500-9ab8-649f586aef1b-9d8cc44e; QN244=QWBLX_admin07; QN247=1530846880416; QN245=af009580f7e87cae77aa01c69465c012b04373d7'
}


def get_city(city_name):
    city_json = requests.get(
        'http://www.928383.com/booking/render/city/suggest.json?city=' + parse.quote(city_name), headers=header).json()
    if city_json['ret']:
        return True, city_json['data']
    else:
        return False, ''


def search_hotel(city_name, hotel_name, search_time):
    is_ok, city_info = get_city(city_name)
    if is_ok:
        search_data = {
            'cityUrl': city_info[0]['o'],
            'cityName': city_info[0]['c'],
            'q': hotel_name,
            'limit': '0,10',
            'fromDate': search_time[0],
            'toDate': search_time[1],
            'priceSort': 'false',
            'scoreSort': 'false',
        }
        hotel_list = requests.get('http://www.928383.com/booking/hotel/search.json', params=search_data, headers=header).json()
        if hotel_list['ret']:
            return True, hotel_list['data'], city_info[0]['o'], city_info[0]['c']
        else:
            return False, ''


if __name__ == '__main__':
    search_time = ('2018-07-06', '2018-07-07')
    target_data = []

    data_source = pd.DataFrame(pd.read_csv("./.csv", header=1, encoding='utf-8', engine='python'))
    for indexs in data_source.index:
        pd_city = data_source.loc[indexs].values[0]
        pd_hotel = data_source.loc[indexs].values[1]

        is_ok, hotel_data, city_url, city_name = search_hotel(pd_city, pd_hotel, search_time)
        if is_ok:
            if hotel_data['hotelSearchCount'] > 0:
                hotel = hotel_data['hotels'][0]
                hotel_seq = hotel['hdsSeq']
                hotel_name = hotel['hotelName']
                hotel_address = hotel['hotelAddress']
                hotel_url = 'http://www.928383.com/booking/hotel/search.htm?cityCode=%s&toCity=%s&fromDate=%s&toDate=%s&q=%s' % (
                    city_url, parse.quote(city_name, encoding='utf-8'), search_time[0], search_time[1],
                    parse.quote(hotel_name, encoding='utf-8'))
                target_data.extend([pd_hotel, hotel_name, hotel_seq, hotel_address, hotel_url])
            else:
                target_data.extend([pd_hotel, '', '', '', ''])
        else:
            target_data.extend([pd_hotel, '', '', '', ''])

    target_data.sort(key=lambda x: x[2])
    print(target_data)
    pd.DataFrame(target_data, columns=('搜索酒店名称', '去哪儿酒店名称', '去哪儿酒店编号', '去哪酒店地址', '查询网页地址')).to_csv("test.csv", encoding='utf-8', index=False)
