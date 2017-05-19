# coding=utf-8
from datetime import datetime, timedelta

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from utils.get_launch_num_statistics import DomyBoxLaunchNum
from utils.get_receipt_statistics import update_receipt_data
from models import *


class LauncherNumInChina(View):
    def get(self, request):
        end_date = request.GET.get('end_date', '')
        days = request.GET.get('days', '')
        if end_date == '' or days == '':
            return render(request, 'statistics/launch_number.html', {})

        d = DomyBoxLaunchNum(int(days), end_date)
        d.run()
        result = {
            'city_data': d.city_data,
            'province_data': d.province_data,
            'others': d.others,
            'china_sum': d.china_sum,
            'domy2_total': d.domy2_total,
            'domy3_total': d.domy3_total,
            'province_max': d.province_max,
            'error_msg': d.error_msg
        }
        return JsonResponse(result)


def datetime_to_string(date_obj):
    # datetime转换字符串
    return datetime.strftime(date_obj, '%Y-%m-%d')


def int_to_float2(i):
    # int转小数点后2
    return round(i, 2) / 100


class DateReceiptSum(View):
    def get(self, request):
        now = datetime.now()
        yesterday = datetime_to_string(now - timedelta(days=1))
        yesterday_receipt = DateReceiptStatistics.objects.filter(date=yesterday)
        if not yesterday_receipt:
            update_receipt_data()
            yesterday_receipt = DateReceiptStatistics.objects.filter(date=yesterday)

        yesterday_data = {
            'date': datetime_to_string(yesterday_receipt[0].date),
            'category': {
                'app_sum': [int_to_float2(yesterday_receipt[0].app_sum), '应用'],
                'premiere_sum': [int_to_float2(yesterday_receipt[0].premiere_sum), '极清首映'],
                'vip_sum': [int_to_float2(yesterday_receipt[0].vip_sum), 'VIP'],
                'pack_sum': [int_to_float2(yesterday_receipt[0].pack_sum), '商品包'],
                'recharge_sum': [int_to_float2(yesterday_receipt[0].recharge_sum), '充值'],
            },
            'total_sum': int_to_float2(yesterday_receipt[0].total_sum),
        }
        for k, v in yesterday_data['category'].items():
            yesterday_data['category'][k].append(round(v[0] / yesterday_data['total_sum'] * 100, 2))
        receipt_sum = DateReceiptStatistics.objects.filter(date__gte='2016-1-1')
        receipt_sum = receipt_sum.order_by('date')

        date = [datetime_to_string(q.date) for q in receipt_sum]
        app_sum = [int_to_float2(q.app_sum) for q in receipt_sum]
        premiere_sum = [int_to_float2(q.premiere_sum) for q in receipt_sum]
        vip_sum = [int_to_float2(q.vip_sum) for q in receipt_sum]
        pack_sum = [int_to_float2(q.pack_sum) for q in receipt_sum]
        recharge_sum = [int_to_float2(q.recharge_sum) for q in receipt_sum]
        total_sum = [int_to_float2(q.total_sum) for q in receipt_sum]

        return render(request, 'statistics/receipt_sum.html', {
            'yesterday_data': yesterday_data,
            'date': date,
            'app_sum': app_sum,
            'premiere_sum': premiere_sum,
            'vip_sum': vip_sum,
            'pack_sum': pack_sum,
            'recharge_sum': recharge_sum,
            'total_sum': total_sum,
        })
