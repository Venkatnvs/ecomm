from django.shortcuts import render
from store.utilitys import GetCartData

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