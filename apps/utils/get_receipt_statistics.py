# -*- coding: utf-8 -*-
# @Time    : 17/5/17 下午1:42
# @Author  : wxy
# @File    : get_receipt_statistics.py

import requests
from datetime import datetime, timedelta
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "domyprototype.settings")  # project_name 项目名称
django.setup()
from statistics.models import DateReceiptStatistics

# 产品类型
product_type = {
    '1003': 'app',
    '2006': 'premiere',
    '2009': 'vip',
    '21693': 'pack',
    'recharge': 'recharge',
}
# 支付方式
pay_way = {
    3: 'alipay',
    4: 'weixin',
    7: 'jdpay',
}


def request_data(date):
    url = 'http://cms.finance.pthv.gitv.tv/receipt/getList.json'
    params = {
        'startReceiptDate': date,
        'endReceiptDate': date,
    }

    r = requests.get(url, params=params)
    result = r.json()

    if len(result) == 0:
        return False

    cleaned_data = {
        'date': date,
        'app_sum': 0,
        'premiere_sum': 0,
        'vip_sum': 0,
        'pack_sum': 0,
        'recharge_sum': 0,
        'total_sum': 0,
    }
    for d in product_type:
        temp_product_sum = 0
        for item in result:
            if item['productType'] == d:
                temp_product_sum += item['totalAmount']
        cleaned_data[product_type[d] + '_sum'] = temp_product_sum
        cleaned_data['total_sum'] += temp_product_sum

    return cleaned_data


def update_receipt_data():
    pattern = '%Y-%m-%d'
    now = datetime.now()
    for x in xrange(1, 2000):
        that_day = now - timedelta(days=x)
        target_date = datetime.strftime(that_day, pattern)

        # 获取日期的统计输入
        date_receipt, has_date_data = DateReceiptStatistics.objects.get_or_create(date=target_date)

        # 存在数据不重复保存
        if not has_date_data:
            print '该日期数据存在'
            print datetime.strftime(date_receipt.date, '%Y-%m-%d') + ':', date_receipt.total_sum
            break

        # 存储数据到数据库
        cleaned_data = request_data(target_date)
        if cleaned_data:
            date_receipt.date = cleaned_data['date']
            date_receipt.app_sum = cleaned_data['app_sum']
            date_receipt.pack_sum = cleaned_data['pack_sum']
            date_receipt.premiere_sum = cleaned_data['premiere_sum']
            date_receipt.vip_sum = cleaned_data['vip_sum']
            date_receipt.recharge_sum = cleaned_data['recharge_sum']
            date_receipt.total_sum = cleaned_data['total_sum']

            date_receipt.save()

            print target_date + ' total sum:' + str(cleaned_data['total_sum'])
        else:
            print target_date + ' no data'
            return


if __name__ == '__main__':
    update_receipt_data()
