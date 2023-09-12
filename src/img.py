from django.shortcuts import HttpResponse
import requests
import os
import numpy as np
import cv2 as cv
import urllib
import base64
from PIL import Image
import uuid
import io

def imgfun(data):
    print(data)
    id = uuid.uuid1()
    path = 'C://Users//MURALI//Desktop//store//venv//ecomm//staticfiles//src//'
    req = urllib.request.urlopen(data['url'])
    a = np.array(bytearray(req.read()), dtype=np.uint8)
    img = cv.imdecode(a, cv.IMREAD_UNCHANGED)
    try:
        msk = img[:,:,3]==0
        re = data['colour'].lstrip('#')
        rgb = list(int(re[i:i+2], 16) for i in (0,2,4))
        rgb.append(255)
        print(rgb)
        img[msk] = rgb
    except Exception as e:
        print(e)
    img = cv.resize(img, (int(data['width']), int(data['hight'])))
    bb = cv.detailEnhance(img, sigma_s=100, sigma_r=0.01)
    aa = cv.imwrite(path+id.hex+'_image.jpg', bb)
    # con = base64.b64encode(requests.get(url).content)
    with open(path+id.hex+'_image.jpg', 'rb') as images:
        con = base64.b64encode(images.read())
    with open(path+id.hex+'_encode.bin', 'wb') as file:
        file.write(con)
    os.remove(path+id.hex+'_image.jpg')
    return con.decode('utf-8')

def img2fun(value):
    d = base64.b64encode(requests.get(value['url']).content)
    b = io.BytesIO()
    imd = base64.b64decode(d)
    img = Image.open(io.BytesIO(imd))
    new_img = img.resize((int(value['width']), int(value['hight'])), Image.ANTIALIAS)
    new_img.save(b, format='PNG', quality=1)
    a = base64.b64encode(b.getvalue())
    return a.decode('utf-8')


