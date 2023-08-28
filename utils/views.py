from django.shortcuts import render
from store.utilitys import GetCartData
from urllib.parse import urlparse
import os
from django.http import HttpResponse

def HelpPage(request):
    data_uts = GetCartData(request)
    context = {
        'items':data_uts['items'],
        'order':data_uts['order'],
        }
    return render(request,'utils/help_pg.html',context)

def ContactPage(request):
    data_uts = GetCartData(request)
    context = {
        'items':data_uts['items'],
        'order':data_uts['order'],
        }
    return render(request,'utils/contact_page.html',context)

def ProfilePage(request):
    data_uts = GetCartData(request)
    context = {
        'items':data_uts['items'],
        'order':data_uts['order'],
        }
    return render(request,'utils/account.html',context)

def TermsConditions(request):
    return render(request,"utils/terms_and_conditions.html")

def ViewLog(request):
    log_file_path = 'logs/debug.log'  # Update this to your log file path
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as log_file:
            log_content = log_file.read()
    else:
        log_content = "Log file not found."
    return HttpResponse(log_content, content_type='text/plain')