from django.shortcuts import render, HttpResponse
from django.http import StreamingHttpResponse,JsonResponse,FileResponse
from .img import imgfun, img2fun
from .models import image
import uuid
import numpy as np
import cv2 as cv
import urllib
import os
import base64
from PIL import Image, ImageDraw, ImageFont
import io
import requests
from django.conf.urls.static import static
from django.conf import settings
import jsonpickle
import json
from django.views.static import serve


# Create your views here.
def main(request):
    if request.method == "GET":
        return render(request, 'ctm_admin/test.html')
    if request.method == 'POST':
        a = imgfun(request.POST)
        b = img2fun(request.POST)
        return render(request, 'ctm_admin/test.html', {'a':a,'b':b,'value':request.POST})

def main2(request):
    if request.method == "GET":
        return render(request, 'ctm_admin/test.html')

def post_imd(request):
    id = uuid.uuid1()
    path = 'C://Users//MURALI//Desktop//store//venv//ecomm//staticfiles//src//'
    req = urllib.request.urlopen(request.GET.get('url','http://127.0.0.1:8000/media/categories/uploads/2022/09/05/69c6589653afdb9a.jpg'))
    a = np.array(bytearray(req.read()), dtype=np.uint8)
    img = cv.imdecode(a, cv.IMREAD_UNCHANGED)
    img = cv.resize(img, (int(request.GET.get('w',200)), int(request.GET.get('h',200))))
    try:
        msk = img[:,:,3]==0
        re = request.GET.get('col','000000')
        rgb = list(int(re[i:i+2], 16) for i in (4,2,0))
        rgb.append(255)
        print(rgb)
        img[msk] = rgb
    except Exception as e:
        print(e)
    aa = cv.imwrite(path+id.hex+'_image.jpg', img)
    with open(path+id.hex+'_image.jpg', 'rb') as images:
        return HttpResponse(images.read(), content_type='image/jpeg;')

def post_imd3(request):
    print(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
    id = uuid.uuid1()
    path = 'C://Users//MURALI//Desktop//store//venv//ecomm//staticfiles//src//'
    req = urllib.request.urlopen(request.GET.get('url','http://127.0.0.1:8000/media/categories/uploads/2022/09/05/69c6589653afdb9a.jpg'))
    a = np.array(bytearray(req.read()), dtype=np.uint8)
    img = cv.imdecode(a, cv.IMREAD_UNCHANGED)
    img = cv.resize(img, (int(request.GET.get('w',200)), int(request.GET.get('h',200))))
    try:
        msk = img[:,:,3]==0
        re = request.GET.get('col','000000')
        rgb = list(int(re[i:i+2], 16) for i in (4,2,0))
        rgb.append(255)
        print(rgb)
        img[msk] = rgb
    except Exception as e:
        print(e)
    col_pill = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    b = io.BytesIO()
    new_img = Image.fromarray(col_pill)
    w, h = new_img.size
    draw = ImageDraw.Draw(new_img)
    text=str(request.GET.get('wm-txt','NVS Watermark'))
    font = ImageFont.truetype('arial.ttf',int(request.GET.get('wm-fs',10)))
    tw, th = draw.textsize(text, font)
    re = request.GET.get('wm-cl','000000')
    rgb = tuple(int(re[i:i+2], 16) for i in (0,2,4))
    mx = int(request.GET.get('wm-mrx',10))
    my = int(request.GET.get('wm-mry',10))
    x = w - tw - mx
    y = h - th - my
    draw.text((x,y), text, rgb, font=font)
    new_img.save(b, 'png', quality=int(request.GET.get('q',40)), optimize=True, lossless=False)
    print(b.getbuffer().nbytes)
    img_c = b.getvalue()
    b.flush()
    b.seek(0)
    b.close()
    return HttpResponse(img_c, content_type='image/jpeg')
    # aa = cv.imwrite(path+id.hex+'_image.jpg', img)
    # with open(path+id.hex+'_image.jpg', 'rb') as images:
    #     return HttpResponse(images.read(), content_type='image/jpeg;')

from .post_4_working import main

def post_imd4(request, path):
    try:
        img_c = main(request, path)
        response = HttpResponse(content_type ="image/png")
        response['Content-Disposition'] = "filename*=utf-8''main.png"
        response.write(img_c)
        return response
    except Exception as e:
        return JsonResponse({'error':'Not Found','message':jsonpickle.encode(e),},safe=False)
        red = Image.new('RGBA', (1, 1), (255,0,0,0))
        response = HttpResponse(content_type="image/png")
        red.save(response, "png")
        return response

def post_img2(request):
    d = base64.b64encode(requests.get(request.GET.get('url','http://127.0.0.1:8000/media/categories/uploads/2022/09/05/69c6589653afdb9a.jpg')).content)
    b = io.BytesIO()
    imd = base64.b64decode(d)
    img = Image.open(io.BytesIO(imd))
    new_img = img.resize((int(request.GET.get('w',200)), int(request.GET.get('h',200))), Image.ANTIALIAS)
    w, h = new_img.size
    draw = ImageDraw.Draw(new_img)
    text=str(request.GET.get('wm-txt','NVS Watermark'))
    font = ImageFont.truetype('arial.ttf',int(request.GET.get('wm-fs',10)))
    tw, th = draw.textsize(text, font)
    re = request.GET.get('wm-cl','000000')
    rgb = tuple(int(re[i:i+2], 16) for i in (0,2,4))
    mx = int(request.GET.get('wm-mrx',10))
    my = int(request.GET.get('wm-mry',10))
    x = w - tw - mx
    y = h - th - my
    draw.text((x,y), text, rgb, font=font)
    new_img.save(b, 'png', quality=int(request.GET.get('q',40)), optimize=True, lossless=False)
    print(b.getbuffer().nbytes)
    img_c = b.getvalue()
    b.flush()
    b.seek(0)
    b.close()
    return HttpResponse(img_c, content_type='image/jpeg')

def getimage(request):
    img = image.objects.all()
    if request.method == "GET":
        return render(request, 'ctm_admin/test2.html', {'imgs':img})
    # if request.method == 'POST':
    #     a = imgfun(request.POST['url'])
    #     return render(request, 'ctm_admin/test.html', {'a':a})

from .ctmserver import MainCtm

def ImageCtmServer(request,path):
    try:
        response = HttpResponse(content_type ="image/png")
        # response['Content-Disposition'] = "filename*=utf-8''main.png"
        response = MainCtm(request, path,response)
        # response.write(img_c)
        return response
    except Exception as e:
        base_path = os.path.join(settings.BASE_DIR,'media')
        # base_path = os.path.join(base_path,'categories','uploads')
        return serve(request,path,document_root=base_path)
        # return JsonResponse({'error':'Not Found','message':jsonpickle.encode(e),},safe=False)
        # red = Image.new('RGBA', (1, 1), (255,0,0,0))
        # response = HttpResponse(content_type="image/png")
        # red.save(response, "png")
        # return response