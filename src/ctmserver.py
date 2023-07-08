from django.conf import settings
import os
import cv2 as cv
import io
from PIL import Image,ImageDraw,ImageFont
from django.views.static import serve
import mimetypes
import posixpath
from pathlib import Path
from django.http import FileResponse, Http404, HttpResponseNotModified,HttpResponse
from django.utils._os import safe_join
from django.utils.http import http_date, parse_http_date
from django.utils.translation import gettext as _

def DefaultImg(request,response,path,base_path):
    print(f'############{path}')
    return serve(request,path,document_root=base_path)
    # with open(img_path, "rb") as f:p
    #     response.write(f.read())
    # return response

def CvChanges(img_path):
    img = cv.imread(img_path, cv.IMREAD_UNCHANGED)
    im_resize = cv.resize(img, (100, 100))
    is_success, im_buf_arr = cv.imencode(".jpg", im_resize)
    io_buf = io.BytesIO(im_buf_arr)
    byte_im = io_buf.getvalue()
    return byte_im

def MainCtm(request,path,response):
    base_path = os.path.join(settings.BASE_DIR,'media')
    # base_path = os.path.join(base_path,'categories','uploads')
    img_path = os.path.join(base_path, path)
    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(img_path)
    print(f'_____________ {os.path.basename(img_path)}')
    try :
        # byte_im = PilChanges(img_path)
        # response.write(byte_im)
        response = DefaltCtmServe(request,path,base_path)
        return response
    except Exception as e:
        print(e)
        return DefaultImg(request,response,path,base_path)
    
def PilChanges(request,fullpath):
    im = Image.open(fullpath).convert("RGBA")
    resizeh = int(request.GET.get('h',False))
    resizew = int(request.GET.get('w',False))
    if resizeh and resizew:
        im = im.resize((400,400))
    bgtp = request.GET.get('bg-tp',False)
    if bgtp=="t":
        newImage = []
        for item in im.getdata():
            if item[:3] == (255, 255, 255):
                newImage.append((255, 255, 255, 0))
            else:
                newImage.append(item)
        im.putdata(newImage)
    buf = io.BytesIO()
    w, h = im.size
    bgcl = request.GET.get('bg-cl',False)
    draw = ImageDraw.Draw(im)
    text=str(request.GET.get('wm-txt','NvsTrades'))
    font = ImageFont.truetype('arial.ttf',int(request.GET.get('wm-fs',w*0.02)))
    tw, th = draw.textsize(text, font)
    wmcl = request.GET.get('wm-cl',False)
    mx = int(request.GET.get('wm-mrx',w*0.04))
    my = int(request.GET.get('wm-mry',h*0.04))
    x = w - tw - mx
    y = h - th - my
    if wmcl:
        rgb = tuple(int(wmcl[i:i+2], 16) for i in (0,2,4))
        draw.text((x,y), text,rgb,font=font)
    else:
        draw.text((x,y), text,(0, 0, 0, 128),font=font)
    if bgcl:
        rgb = tuple(int(bgcl[i:i+2], 16) for i in (0,2,4))
        new_image = Image.new("RGB", (w, h), rgb)
        new_image.paste(im, (0, 0), mask=im)
        im = new_image
    im.save(buf, format='PNG')
    buf.seek(0)
    return buf

def DefaltCtmServe(request, path, document_root=None):
    path = posixpath.normpath(path).lstrip("/")
    fullpath = Path(safe_join(document_root, path))
    if fullpath.is_dir():
        raise Http404(_("Directory indexes are not allowed here."))
    if not fullpath.exists():
        raise Http404(_("“%(path)s” does not exist") % {"path": fullpath})
    # Respect the If-Modified-Since header.
    statobj = fullpath.stat()
    if not was_modified_since(
        request.META.get("HTTP_IF_MODIFIED_SINCE"), statobj.st_mtime
    ):
        return HttpResponseNotModified()
    content_type, encoding = mimetypes.guess_type(str(fullpath))
    content_type = content_type or "application/octet-stream"
    buf = PilChanges(request,fullpath)
    response = FileResponse(buf, content_type=content_type)
    # response = FileResponse(fullpath.open("rb"), content_type=content_type)
    response.headers["Last-Modified"] = http_date(statobj.st_mtime)
    if encoding:
        response.headers["Content-Encoding"] = encoding
    return response


def was_modified_since(header=None, mtime=0):
    try:
        if header is None:
            raise ValueError
        header_mtime = parse_http_date(header)
        if int(mtime) > header_mtime:
            raise ValueError
    except (ValueError, OverflowError):
        return True
    return False
