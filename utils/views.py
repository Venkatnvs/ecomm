from django.shortcuts import render
from store.utilitys import GetCartData
from urllib.parse import urlparse

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