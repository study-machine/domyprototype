# coding=utf-8
import requests
import uniout
import json
import re
from datetime import datetime, timedelta

from django.shortcuts import render
from django.views.generic import View

from utils.geo_result import GEO_RESULT


class LauncherNumInChina(View):
    def get(self, request):
        data = self.get_statistics_data(1)
        json_for_map, cleaned_data, others = self.parse_statistics_data(data)
        json_for_map = json.dumps(json_for_map)
        return render(request, 'statistics/launch_num.html', {
            'json_for_map': json_for_map,
            'cleaned_data': cleaned_data,
            'others': others,
            'domy2_total': self.domy2_total,
            'domy3_total': self.domy3_total,
        })

    def get_statistics_data(self, days):
        url = 'http://display.data.pthv.gitv.tv/data_display/stat/graph.json?' \
              '&trCode=0000_06012_201_cp&organQueryType=cp_channel&cp_channel=-9998&CP_CHANNEL=-9998&REPORTTYPE=day' \
              'day&STARTTIME={0}&ENDTIME={1}'

        now_date = datetime.now()
        start_date = (now_date - timedelta(days=days)).strftime('%Y-%m-%d')
        end_date = (now_date - timedelta(days=days)).strftime('%Y-%m-%d')
        url = url.format(start_date, end_date)

        r = requests.get(url)
        j_res = r.json()
        data = [(x[0], int(x[1]), int(x[2])) for x in
                zip(j_res['groups'], j_res['datainfo'][0]['data'], j_res['datainfo'][1]['data'])]
        self.domy2_total = sum(map(lambda _: int(_), j_res['datainfo'][0]['data']))
        self.domy3_total = sum(map(lambda _: int(_), j_res['datainfo'][1]['data']))
        return data

    def parse_statistics_data(self, data):
        # 数据清理
        cleaned_data = []
        for item in data:
            cleaned_data.append({
                'company': item[0].encode('utf-8'),
                'city': self.is_city(item[0]),
                'domy2': item[1],
                'domy3': item[2]
            })
        # 数据分组
        others = []
        data_for_map = {}
        for x in cleaned_data:
            city_name, company_name = x['city'], x['company']
            domy2_num, domy3_num = x['domy2'], x['domy3']
            com_data = {'company': company_name, 'domy2': domy2_num, 'domy3': domy3_num}
            if city_name == 0:
                # 无城市数据
                others.append([company_name, domy2_num, domy3_num])
                continue
            if data_for_map.get(city_name):
                # 同城市分公司数据
                data_for_map[city_name][2].append(com_data)
            else:
                # 获取经纬度
                lng, lat = GEO_RESULT[city_name][0], GEO_RESULT[city_name][1]
                data_for_map[city_name] = [lng, lat, [com_data, ]]

        # 转地图需要的格式
        json_for_map = [{'name': k, 'value': v} for k, v in data_for_map.items()]
        # 地图外数据排序
        others = sorted(others, lambda x, y: (x[1] + x[2]) - (y[1] + y[2]))
        return json_for_map, cleaned_data, others

    def is_city(self, u_name):
        pattern = r'^(.*)(长城宽带|长宽|鹏博士|长宽宽带|电信通|宽带通|中邦亚通)$'
        com_re = re.match(pattern, u_name.encode('utf-8'))
        if com_re:
            return com_re.group(1) + '市'
        else:
            return 0
