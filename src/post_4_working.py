
import cv2 as cv
import urllib
import os
import base64
from PIL import Image, ImageDraw, ImageFont
import io
import requests
from django.conf.urls.static import static
from django.conf import settings

def main(request, path):
    base_path = os.path.join(settings.BASE_DIR,'media')
    base_path = os.path.join(base_path,'categories')
    base_path = os.path.join(base_path,'uploads')
    img_path = os.path.join(base_path, path)
    img = cv.imread(img_path, cv.IMREAD_UNCHANGED)
    img = cv.resize(img, (int(request.GET.get('w',200)), int(request.GET.get('h',200))))
    b = io.BytesIO()
    if request.GET.get('is-bg', 'f') == 't':
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
    new_img = Image.fromarray(col_pill)
    if request.GET.get('is-wm', 'f') == 't':
        w, h = new_img.size
        draw = ImageDraw.Draw(new_img)
        text=str(request.GET.get('wm-txt','NVS Watermark'))
        font = ImageFont.truetype('arial.ttf',int(request.GET.get('wm-fs',10)))
        tw, th = draw.textsize(text, font)
        re = request.GET.get('wm-cl','ffffff')
        rgb = tuple(int(re[i:i+2], 16) for i in (0,2,4))
        mx = int(request.GET.get('wm-mrx',10))
        my = int(request.GET.get('wm-mry',10))
        x = w - tw - mx
        y = h - th - my
        draw.text((x,y), text, rgb, font=font)
    new_img.save(b, 'png', quality=int(request.GET.get('q',40)), optimize=True, lossless=False)
    img_c = b.getvalue()
    b.flush()
    b.seek(0)
    b.close()
    return img_c