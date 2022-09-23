from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.conf import settings
import os
import json

# Create your views here.
def state_dist(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        if search_str == 'Choose...':
            data_a = {'not_state'}
            return JsonResponse(list(data_a), safe=False)
        file_path = os.path.join(settings.BASE_DIR, 'states_dist.json')
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            for v in data:
                x = v['state']
                if x == search_str:
                    data_dist = v['districts']
        data_a = data_dist
        return JsonResponse(list(data_a), safe=False)


def main(request):
    client_logged = ''
    print(request.user)
    if request.user == 'AnonymousUser':
        client_logged = 0
    check = User.objects.filter(username=request.user).exists()
    if check:
        user_details = User.objects.get(username=request.user)
        client_logged = 1
    else:
        user_details = ''
    context = {
        'client' : user_details,
        'client_logged': client_logged,
    }
    return render(request, 'main/index.html', context)


def Cart(request):
    check = User.objects.filter(username=request.user).exists()
    if check:
        user_details = User.objects.get(username=request.user)
    else:
        user_details = ''
    context = {
        'client' : user_details
    }
    return render(request, 'main/cart.html', context)


def Checkout(request):
    states_data = []
    file_path = os.path.join(settings.BASE_DIR, 'states_dist.json')
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for values in data:
            states_data.append(values['state'])
    client_logged = ''
    print(request.user)
    if request.user == 'AnonymousUser':
        client_logged = 0
    check = User.objects.filter(username=request.user).exists()
    if check:
        user_details = User.objects.get(username=request.user)
        client_logged = 1
    else:
        user_details = ''
    context = {
        'client' : user_details,
        'client_logged': client_logged,
        'data': states_data
    }
    return render(request, 'main/checkout.html', context)
