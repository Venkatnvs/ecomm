import os
from django.conf import settings
import random
import json
import datetime
import wikipedia
import requests
import pyjokes

def voice_process(request):
    file_path = os.path.join(settings.BASE_DIR, 'data_files/results.json')
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
                        break
                data = f"opening {a}"
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
        elif 'who is' in query:
            query = query.replace("who is", "")
            results = wikipedia.summary(query, sentences=1)
            w_rep = "According to Wikipedia" + results
            d_type = 'data'
            data = w_rep
        elif 'play' in query:
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
            data = f"Playing {query}"
            d_type = 'url'
            id_data = str(lst[count - 5])
            id = id_data.replace("watch",'').replace("?v=",'')
            u_content = f"{request.scheme}://{request.META['HTTP_HOST']}/voice/d/yt{id}"

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            d_type = 'data'
            data = f"the time is {strTime}"
        elif 'joke' in query:
            d_type = 'data'
            data = pyjokes.get_joke()
        elif 'hi' in query or 'hello' in query:
            d_type = 'data'
            for v in datas:
                if v['question'] == 'urls':
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
        return data_a

def voice_ws_process(Search_data):
    file_path = os.path.join(settings.BASE_DIR, 'data_files/results.json')
    with open(file_path, 'r') as json_file:
        datas= json.load(json_file)
    f_data = Search_data
    query = f_data.lower()
    if 'open' in query:
        d_type = 'url'
        for v in datas:
            if v['question'] == 'urls':
                a_b = v['answer']
        for d in a_b:
            print('1 '+str(d))
            for a in d:
                if a in query:
                    print(d[a])
                    a_d_a = d[a]
                    data = f"opening {a}"
                    u_content = a_d_a
                    break
                else:
                    temp = query.replace(' ','+')
                    g_url="https://www.google.com/search?q="
                    res_g = 'sorry! i cant understand but i search from internet to give your answer.'
                    data = res_g
                    u_content = g_url+temp
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
        a_a='your name is '
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
    elif 'who is' in query:
        query = query.replace("who is", "")
        results = wikipedia.summary(query, sentences=1)
        w_rep = "According to Wikipedia" + results
        d_type = 'data'
        data = w_rep
    elif 'play' in query:
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
        data = f"Playing {query}"
        d_type = 'url'
        id_data = str(lst[count - 5])
        id = id_data.replace("watch",'').replace("?v=",'')
        u_content = f"http://10.62.16.77:8000/voice/d/yt{id}"
    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")    
        d_type = 'data'
        data = f"the time is {strTime}"
    elif 'joke' in query:
        d_type = 'data'
        data = pyjokes.get_joke()
    elif 'hi' in query or 'hello' in query:
        d_type = 'data'
        for v in datas:
            if v['question'] == 'urls':
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
    return data_a