#!/usr/bin/env python

import datetime
import os 
import time
from datetime import date, timedelta
import json
import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import datetime
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers import serialize

   
def dashboard(request):
    return render(request, 'dashboard.html')

def addproduct(request):

    return render(request, 'addproduct.html')

def viewproduct(request):
    result = ProductTable.objects.all()
    # print(result)
    return render(request, 'viewproduct.html',{'number':result})

@csrf_exempt
def add_product_api(request):
    print('fdsfsdfsd')
    
    product_name = request.POST['product_name']
    product_desc = request.POST['product_desc']
    
    product_data = ProductTable(product_id=None, name = product_name, description = product_desc,  is_active='Y', status='ACTIVE')
    product_data.save()

    response_action = False
    response_data = ""
    status = False
    result = {}

    result['response_action'] = response_action
    result['response_data']   = response_data
    return HttpResponse(json.dumps(result))

@csrf_exempt
def search_product_api(request):
 
    result = ProductTable.objects.get()
 
    return HttpResponse(json.dumps(result))

@csrf_exempt
def get_product_api(request):
    result= []

    # search_term = request.POST.get('search_term', None)   
    # if search_term!='':
    #     # print(search_term)
    # else:
    #     result = ProductTable.objects.all()
    
    result = ProductTable.objects.all()
    result = serializers.serialize('json', result)
    return HttpResponse(result, content_type='application/json')