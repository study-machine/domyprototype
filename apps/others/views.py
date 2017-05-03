from django.shortcuts import render
from django.views.generic import View

from .models import *


class IntroductionView(View):
    def get(self, request):
        all_versions = Version.objects.all()
        return render(request, 'introduction.html', {
            'all_versions': all_versions
        })
