from django.shortcuts import render, HttpResponse
import json
import wikipedia
import pyjokes
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
import random

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

def dgdgdgdgd(request):
    return render(request, 'voice/main.html')


def redirecturl(request):
    return render(request,'voice/redirecturl.html')


@csrf_exempt
def json_voice2(request):
    file_path = os.path.join(settings.BASE_DIR, 'voice/results.json')
    with open(file_path, 'r') as json_file:
        datas= json.load(json_file)
    if request.method == 'POST':
        f_data = json.loads(request.body).get('searchText')
        query = f_data.lower()
        if 'open' in query:
            for v in datas:
                if v['question'] == 'urls':
                    a_b = v['answer']
            for d in a_b:
                print('1 '+str(d))
                for a in d:
                    if a in query:
                        print(d[a])
                        a_d_a = d[a]
                data = 'opening '
                # data = 'opening '+str(a)+'.'
                d_type = 'url'
                u_content = a_d_a
        elif "today's date" in query or 'date today' in query:
            now = datetime.datetime.now()
            aab = now.strftime("%d-%m-%Y")
            d_type = 'data'
            data = aab
        elif "today's day" in query or 'day is' in query:
            now = datetime.datetime.now()
            aaa = now.strftime("%A")
            d_type = 'data'
            data = aaa
        elif 'my name' in query:
            a_a='your name is ' + str(request.user)
            d_type = 'data'
            data = a_a
        # elif 'open youtube' in query:
        #     data_a = {'type':'url', 'URL':'https://youtube.com', 'content':'opening youtube'}
        elif 'wikipedia' in query:
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            w_rep = "According to Wikipedia" + results
            d_type = 'data'
            data = w_rep
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            time_rep = f"the time is {strTime}"
            d_type = 'data'
            data = time_rep
        elif 'joke' in query:
            joke_rep = pyjokes.get_joke()
            d_type = 'data'
            data = joke_rep
        elif 'hi' in query:
            d_type = 'data'
            data = random.choice(v['answer'])
        else:
            temp = query.replace(' ','+')
            g_url="https://www.google.com/search?q="
            res_g = 'sorry! i cant understand but i search from internet to give your answer.'
            data = res_g
            d_type = 'url'
            u_content = g_url+temp
        if d_type == 'url':
            data_a = {'type':d_type, 'URL':u_content, 'content':data}
        else:
            data_a = {'type':d_type, 'content':data}
        return JsonResponse(data_a, safe=False)
