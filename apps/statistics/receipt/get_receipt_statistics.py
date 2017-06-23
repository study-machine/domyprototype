# -*- coding: utf-8 -*-
# @Time    : 17/5/17 下午1:42
# @Author  : wxy
# @File    : get_receipt_statistics.py
from collections import OrderedDict
from datetime import datetime, timedelta

import requests

from ..models import DateReceiptStatistics

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


def datetime_to_string(date_obj):
    # datetime转换字符串
    return datetime.strftime(date_obj, '%Y-%m-%d')


def fen_to_yuan(i):
    # 分转化元,int转小数点后2
    return round(i, 2) / 100


def request_data(date):
    # 从大麦财务接口获取收款数据
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


class DomyReceiptStatistics(object):
    def __init__(self, start_date):
        """获取大麦盒子收款金额数据"""
        self.yesterday = ''
        self.yesterday_data = {}
        self.start_date = start_date
        self.history_date = {}
        self.history_month = {}
        self.run()

    def run(self):
        yesterday_qs = self.__has_yesterday_data()

        if not yesterday_qs:
            update_receipt_data()
            yesterday_qs = DateReceiptStatistics.objects.filter(date=self.yesterday)

        self.__parse_yesterday_data(yesterday_qs)
        print self.yesterday_data

    def __has_yesterday_data(self):
        # 判断是否有昨天的数据
        now = datetime.now()
        self.yesterday = datetime_to_string(now - timedelta(days=1))
        yesterday_receipt = DateReceiptStatistics.objects.filter(date=self.yesterday)
        return yesterday_receipt

    def __parse_yesterday_data(self, yesterday_qs):
        yesterday_data = {
            'date': datetime_to_string(yesterday_qs[0].date),
            'category': {
                'app_sum': [fen_to_yuan(yesterday_qs[0].app_sum), '应用'],
                'premiere_sum': [fen_to_yuan(yesterday_qs[0].premiere_sum), '极清首映'],
                'vip_sum': [fen_to_yuan(yesterday_qs[0].vip_sum), 'VIP'],
                'pack_sum': [fen_to_yuan(yesterday_qs[0].pack_sum), '商品包'],
                'recharge_sum': [fen_to_yuan(yesterday_qs[0].recharge_sum), '充值'],
            },
            'total_sum': fen_to_yuan(yesterday_qs[0].total_sum),
        }
        for k, v in yesterday_data['category'].items():
            yesterday_data['category'][k].append(round(v[0] / yesterday_data['total_sum'] * 100, 2))

        self.yesterday_data = yesterday_data

    @staticmethod
    def get_history_qs(start_date):
        return DateReceiptStatistics.objects.filter(date__gte=start_date).order_by('date')

    def get_history_data(self):
        # 根据起始日期获取历史数据
        history_qs = self.get_history_qs(self.start_date)
        self.start_date = datetime_to_string(history_qs[0].date)
        self.__parse_date_history(history_qs)
        self.__parse_month_history(history_qs)

    def __parse_date_history(self, receipt_qs):
        # 转化日收入数据
        self.history_date = {
            'date': [datetime_to_string(q.date) for q in receipt_qs],
            'app_sum': [fen_to_yuan(q.app_sum) for q in receipt_qs],
            'premiere_sum': [fen_to_yuan(q.premiere_sum) for q in receipt_qs],
            'vip_sum': [fen_to_yuan(q.vip_sum) for q in receipt_qs],
            'pack_sum': [fen_to_yuan(q.pack_sum) for q in receipt_qs],
            'recharge_sum': [fen_to_yuan(q.recharge_sum) for q in receipt_qs],
            'total_sum': [fen_to_yuan(q.total_sum) for q in receipt_qs],
        }

    def __parse_month_history(self, receipt_qs):
        # 转化月收入数据
        month_receipt = OrderedDict()
        for q in receipt_qs:
            month_str = str(q.date.year) + '-' + str(q.date.month)
            if month_str not in month_receipt:
                month_receipt[month_str] = {
                    'app_sum': q.app_sum,
                    'premiere_sum': q.premiere_sum,
                    'vip_sum': q.vip_sum,
                    'pack_sum': q.pack_sum,
                    'recharge_sum': q.recharge_sum,
                    'total_sum': q.total_sum,
                }
            else:
                month_receipt[month_str]['app_sum'] += q.app_sum
                month_receipt[month_str]['premiere_sum'] += q.premiere_sum
                month_receipt[month_str]['vip_sum'] += q.vip_sum
                month_receipt[month_str]['pack_sum'] += q.pack_sum
                month_receipt[month_str]['recharge_sum'] += q.recharge_sum
                month_receipt[month_str]['total_sum'] += q.total_sum

        self.history_month = {
            'month': [k for k in month_receipt],
            'app_sum': [fen_to_yuan(v['app_sum']) for v in month_receipt.values()],
            'premiere_sum': [fen_to_yuan(v['premiere_sum']) for v in month_receipt.values()],
            'vip_sum': [fen_to_yuan(v['vip_sum']) for v in month_receipt.values()],
            'pack_sum': [fen_to_yuan(v['pack_sum']) for v in month_receipt.values()],
            'recharge_sum': [fen_to_yuan(v['recharge_sum']) for v in month_receipt.values()],
            'total_sum': [fen_to_yuan(v['total_sum']) for v in month_receipt.values()],
        }


if __name__ == '__main__':
    # update_receipt_data()
    d = DomyReceiptStatistics()
    d.get_history_data()
    pass
