import requests
from bs4 import BeautifulSoup
import re
import urllib

def get_resp(url):
    headers = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    response = requests.get(url, headers=headers)
    print(response.text)
    return response

def get_images(response):
    images = re.findall('"hiRes":"(.+?)"', response.text)
    new_list = []
    for i in images:
        if i not in new_list:
            new_list.append(i)
    return new_list

def SoupGetInfo(response):
    soup = BeautifulSoup(response.content, "lxml")
    product_name = ''
    product_price = ''
    product_brand = ''
    product_l_details = ''
    try:
        product_title = soup.find("span",attrs={"id": 'productTitle'})
        product_name = product_title.string.strip().replace(',', '')
    except AttributeError:
        product_name = "NA"
    try:
        product_price = soup.find("span", attrs={'class': 'a-offscreen'}).string.strip().replace(',', '')
    except AttributeError:
        product_price = "NA"
    try:
        brand_element = soup.find('a', class_='a-link-normal', id='bylineInfo')
        if brand_element:
            product_brand = brand_element.text.strip().replace('Brand: ','')
    except AttributeError:
        product_brand = "NA"
    try:
        from_man_element = soup.find('div', class_='aplus-v2 desktop celwidget')
        if from_man_element:
            product_l_details = str(from_man_element)
    except AttributeError:
        product_l_details = "NA"
    key = [x.get_text(strip=True).replace('\u200f\n','').replace('\u200e','').replace(':\n','').replace('\n', '').strip() for x in soup.select('ul.a-unordered-list.a-nostyle.a-vertical.a-spacing-none.detail-bullet-list > li > span > span.a-text-bold')][:13]
    value = [x.get_text(strip=True) for x in soup.select('ul.a-unordered-list.a-nostyle.a-vertical.a-spacing-none.detail-bullet-list > li > span > span:nth-child(2)')]
    product_details = {k:v for  k, v, in zip(key, value)}
    return {'p_name':product_name,'p_price':product_price,'p_brand':product_brand,'p_l_det':product_l_details,'p_det_a':product_details}

def get_amazon_product_page(url):
    resp = get_resp(url)
    img_d = get_images(resp)
    title_d = SoupGetInfo(resp)
    return {'img_d':img_d,'ti_info':title_d}