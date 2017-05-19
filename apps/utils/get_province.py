# -*- coding: utf-8 -*-
# @Time    : 17/5/8 上午11:53
# @Author  : wxy
# @File    : get_province.py

import requests
import uniout

from geo_result import GEO_RESULT

url = 'http://api.map.baidu.com/geocoder/v2/?location={0},{1}&output=json&pois=1&ak=uDhP9RHXugAnU03rZE9rfceA8XbLX59y'
province_result = {}
for k,v in GEO_RESULT.items():
    r_url = url.format(v[1],v[0])
    r = requests.get(r_url)
    j_res = r.json()
    province = j_res['result']['addressComponent']['province'].encode('utf-8')
    v.append(province)
    province_result[k]= v

print province_result

