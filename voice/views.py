from django.shortcuts import render, HttpResponse
import json
import wikipedia
import requests
import pyjokes
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
import random
from .process import voice_process

@csrf_exempt
def json_voice(request):
    if request.method == 'POST':
        f_data = json.loads(request.body).get('searchText')
        query = f_data.lower()
        data_a = {}
        if "today's date" in query or 'date today' in query:
            now = datetime.datetime.now()
            aab = now.strftime("%d-%m-%Y")
            data_a = {'type':'data', 'content':aab}
        elif "today's day" in query or 'day is' in query:
            now = datetime.datetime.now()
            aaa = now.strftime("%A")
            data_a = {'type':'data', 'content':aaa}
        elif 'my name' in query:
            a_a='your name is ' + str(request.user)
            data_a = {'type':'data', 'content':a_a}
        elif 'open youtube' in query:
            data_a = {'type':'url', 'URL':'https://youtube.com', 'content':'opening youtube'}
        elif 'wikipedia' in query:
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            w_rep = "According to Wikipedia" + results
            data_a = {'type':'data', 'content':w_rep}
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            time_rep = f"the time is {strTime}"
            data_a = {'type':'data', 'content':time_rep}
        elif 'joke' in query:
            joke_rep = pyjokes.get_joke()
            data_a = {'type':'data', 'content':joke_rep}
        else:
            temp = query.replace(' ','+')
            g_url="https://www.google.com/search?q="
            res_g = 'sorry! i cant understand but i search from internet to give your answer ! okay'
            data_a = {'type':'url', 'URL':g_url+temp, 'content':res_g}
        return JsonResponse(data_a, safe=False)

@csrf_exempt
def wishing(request):
    if request.method == 'GET':
        query = request.GET.get('val',datetime.datetime.now().hour)
        data_a = {}
        try:
            hour = int(query)
        except Exception as e:
            print(e)
        if hour>=0 and hour<12:
            data_a = {'type':'data', 'content':"Good Morning sir ! i am virtual assistent", 'content_next':"Please tell me how may I help you"}
        elif hour>=12 and hour<18:
            data_a = {'type':'data', 'content':"Good Afternoon sir ! i am virtual assistent", 'content_next':"Please tell me how may I help you"}
        else:
            data_a = {'type':'data', 'content':"Good Evening sir ! i am virtual assistent", 'content_next':"Please tell me how may I help you"}
        return JsonResponse(data_a, safe=False)

def main(request):
    return render(request, 'voice/index.html')

def ws_main(request):
    context={
        "voice_group":"base12345"
    }
    return render(request, 'voice/ws/index.html', context)

def dgdgdgdgd(request):
    return render(request, 'voice/main.html')


def redirecturl(request):
    return render(request,'voice/redirecturl.html')


@csrf_exempt
def json_voice2(request):
    data_a = voice_process(request)
    return JsonResponse(data_a, safe=False)


def web_json_voice(request):
    context = {}
    return render(request, '', context)

def youtube_songs(request, query):
    query = query.replace('play','')
    url = f"https://www.youtube.com/results?q={query}"
    count = 0
    cont = requests.get(url)
    data = cont.content
    data = str(data)
    lst = data.split('"')
    for i in lst:
        count += 1
        if i == "WEB_PAGE_TYPE_WATCH":
            break
    if lst[count - 5] == "/results":
        raise Exception("No Video Found for this Topic!")
    # if open_video:
    #     web.open(f"https://www.youtube.com{lst[count - 5]}")
    # return f"https://www.youtube.com{lst[count - 5]}"
    context = {
        'count':count,
        'lst2':lst[count - 5],
        'lst3':lst[count-4]
    }
    return render(request, 'voice/v/youtube_song.html', context)

def json_add(request):
    return render(request, '')

def json_youtube(request, value):
    context = {
        'id': value
    }
    return render(request, 'voice/v/youtube_song.html', context)