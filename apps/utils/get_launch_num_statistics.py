# -*- coding: utf-8 -*-
# @Time    : 17/5/9 上午11:51
# @Author  : wxy
# @File    : get_static_data.py
import requests
import json
import re
import time
from datetime import datetime, timedelta

from .geo_result import province_geo_result


def is_city(u_name):
    # 判断分公司城市
    pattern = r'^(.*)(长城宽带|长宽|鹏博士|长宽宽带|电信通|宽带通|中邦亚通)$'
    com_re = re.match(pattern, u_name.encode('utf-8'))
    if com_re:
        return com_re.group(1) + '市'
    else:
        return 0


class DomyBoxLaunchNum(object):
    def __init__(self, days, end_date):
        self.days = days
        self.end_date = end_date
        self.domy2_total = 0
        self.domy3_total = 0
        self.others = []
        self.city_data = []
        self.province_data = []
        self.china_sum = 0
        self.province_max = 0
        self.error_msg = ''
        self.r_json = {}
        self.url = ''

    def run(self):
        if self.request_data():
            cleaned_data = self.clean_data(self.r_json)
            if cleaned_data:
                self.get_city_data(cleaned_data)
                self.get_provinces_data(cleaned_data)
                return True

    def request_data(self):
        # 请求接口
        url = 'http://display.data.pthv.gitv.tv/data_display/stat/graph.json?' \
              '&trCode=0000_06012_201_cp&organQueryType=cp_channel&cp_channel=-9998&CP_CHANNEL=-9998&REPORTTYPE=day' \
              '&STARTTIME={0}&ENDTIME={1}'
        pattern = '%Y-%m-%d'
        d_end_date = datetime.strptime(self.end_date, pattern)
        start_date = (d_end_date - timedelta(days=self.days - 1)).strftime(pattern)
        end_date = d_end_date.strftime(pattern)
        self.url = url.format(start_date, end_date)
        r = requests.get(self.url)
        if r.status_code != 200:
            self.error_msg = '访问接口错误'
            return False
        else:
            self.r_json = r.json()
            return True

    def clean_data(self, data):
        if len(data['groups']) == 0:
            self.error_msg = '该日期区间无数据'
            return False
        zip_data = [(x[0], int(x[1]), int(x[2])) for x in
                    zip(data['groups'], data['datainfo'][0]['data'], data['datainfo'][1]['data'])]
        self.domy2_total = sum(map(lambda _: int(_), data['datainfo'][0]['data']))
        self.domy3_total = sum(map(lambda _: int(_), data['datainfo'][1]['data']))

        # 数据清理
        cleaned_data = []
        for item in zip_data:
            city_name = is_city(item[0])
            province_name = province_geo_result[city_name][2] if city_name else 0
            cleaned_data.append({
                'company': item[0].encode('utf-8'),
                'city': city_name,
                'province': province_name,
                'domy2': item[1],
                'domy3': item[2]
            })
        return cleaned_data

    def get_city_data(self, cleaned_data):
        # 数据分组
        others = []
        t_dict = {}
        for x in cleaned_data:
            city_name, company_name = x['city'], x['company']
            domy2_num, domy3_num = x['domy2'], x['domy3']
            com_data = {'company': company_name, 'domy2': domy2_num, 'domy3': domy3_num}
            if city_name == 0:
                # 非城市数据
                others.append([company_name, domy2_num, domy3_num])
                continue
            if t_dict.get(city_name):
                # 同城市分公司数据
                t_dict[city_name][2].append(com_data)
            else:
                # 获取经纬度,lng经,lat纬
                lng, lat = province_geo_result[city_name][0], province_geo_result[city_name][1]
                t_dict[city_name] = [lng, lat, [com_data, ]]

        # 转地图需要的格式
        self.city_data = [{'name': k, 'value': v} for k, v in t_dict.items()]
        # 地图外数据排序
        self.others = sorted(others, lambda d2, d3: (d2[1] + d2[2]) - (d3[1] + d3[2]))

    def get_provinces_data(self, cleaned_data):
        # 数据分组
        t_dict = {}
        for x in cleaned_data:
            province_name, city_name, company_name = x['province'], x['city'], x['company']
            domy2_num, domy3_num = x['domy2'], x['domy3']
            com_data = {'city': city_name, 'domy2': domy2_num, 'domy3': domy3_num}
            if city_name == 0:
                # 无城市数据
                continue
            if t_dict.get(province_name):
                # 同城市分公司数据
                t_dict[province_name][1] += domy2_num + domy3_num
                t_dict[province_name][0].append(com_data)
                t_dict[province_name][2] += domy2_num
                t_dict[province_name][3] += domy3_num
            else:
                province_sum = domy2_num + domy3_num
                t_dict[province_name] = [[com_data, ], province_sum, domy2_num, domy3_num]
        self.province_data = [{'name': k, 'value': v} for k, v in t_dict.items()]
        self.china_sum = sum([i['value'][1] for i in self.province_data])
        self.province_max = max([i['value'][1] for i in self.province_data])
