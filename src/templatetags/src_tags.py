from django import template
import uuid
import urllib
import numpy as np
import cv2 as cv
from django.shortcuts import HttpResponse

register = template.Library()

def Ctm_Img(value):
    id = uuid.uuid1()
    path = 'C://Users//MURALI//Desktop//store//venv//ecomm//staticfiles//src//'
    req = urllib.request.urlopen('http://127.0.0.1:8000'+value)
    a = np.array(bytearray(req.read()), dtype=np.uint8)
    img = cv.imdecode(a, cv.IMREAD_UNCHANGED)
    img = cv.resize(img, (200, 200))
    aa = cv.imwrite(path+id.hex+'_image.jpg', img)
    with open(path+id.hex+'_image.jpg', 'rb') as images:
        return HttpResponse(images.read(), content_type='image/jpeg')
    # return value
register.filter('ctm_img', Ctm_Img)

def Ctm_Img2(value,n):
    req = 'http://127.0.0.1:8000'+value
    src = 'http://127.0.0.1:8000/src/d/post2?url='+req+'&h='+str(n)
    return src
register.filter('ctm_img2', Ctm_Img2)