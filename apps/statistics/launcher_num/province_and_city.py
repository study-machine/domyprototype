# -*- coding: utf-8 -*-
# @Time    : 17/5/22 下午3:50
# @Author  : wxy
# @File    : province_and_city.py

import requests
import re

def abbreviate_province(province_full_name):
    """省份全称转换为缩写"""
    pattern = ur'^(.*)(省)'
    com_re = re.match(pattern, province_full_name.decode('utf-8'))
    if com_re:
        return com_re.group(1).encode('utf-8')
    pattern = ur'^(内蒙古|宁夏|广西|西藏|新疆).*'
    com_re = re.match(pattern, province_full_name.decode('utf-8'))
    if com_re:
        return com_re.group(1).encode('utf-8')


# lat 纬度
# lng 精度
class CityLocation(object):
    """通过百度api获取地理位置数据"""
    baidu_ak = 'uDhP9RHXugAnU03rZE9rfceA8XbLX59y'

    def __init__(self, city_name):
        self.city_name = city_name
        self.jd = 0
        self.wd = 0
        self.province_full_name = ''
        self.province_name = ''
        self.run()

    def run(self):
        self.get_city_geo(self.city_name)
        self.get_province(self.jd, self.wd)
        print self.city_name, self.jd, self.wd, self.province_name, self.province_full_name

    def get_city_geo(self, city_name):
        url = 'http://api.map.baidu.com/geocoder/v2/?address={city}&output=json&ak={ak}'
        r_url = url.format(city=city_name, ak=self.baidu_ak)
        r = requests.get(r_url)
        j_res = r.json()
        self.jd = j_res['result']['location']['lng']
        self.wd = j_res['result']['location']['lat']

    def get_province(self, jd, wd):
        url = 'http://api.map.baidu.com/geocoder/v2/?location={wd},{jd}&output=json&pois=1&ak={ak}'
        r_url = url.format(wd=wd, jd=jd, ak=self.baidu_ak)
        r = requests.get(r_url)
        j_res = r.json()
        self.province_full_name = j_res['result']['addressComponent']['province'].encode('utf-8')
        self.province_name = abbreviate_province(self.province_full_name)


if __name__ == '__main__':
    c = CityLocation('乌鲁木齐市')
