# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from django.shortcuts import render
from pageview.models import page
# Create your views here.
def dashboard( request):
  
    obj=page.objects.get(id=1)
    total=obj.page_index_count-obj.refresh_count
    return JsonResponse({'dashboard': total},safe=False)

    