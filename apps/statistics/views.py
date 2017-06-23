# coding=utf-8

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from .launcher_num.get_launch_num_statistics import DomyBoxLaunchNum
from .receipt.get_receipt_statistics import DomyReceiptStatistics


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


class DateReceiptSum(View):
    def get(self, request):
        start_date = request.GET.get('start_date', '2016-01-01')

        d = DomyReceiptStatistics(start_date)
        d.get_history_data()

        return render(request, 'statistics/receipt_sum.html', {
            'yesterday_data': d.yesterday_data,
            'history_date': d.history_date,
            'history_month': d.history_month,
            'start_date': d.start_date,
        })
