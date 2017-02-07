# coding=utf-8
import urllib2
import re
from django.http import HttpResponse
from app import models
from PIL import Image
import cStringIO
from app import upload_picture_to_oss
from app import get_color
from app import deal_image


def get_images_pixabay_com(request):
    url = "https://pixabay.com/zh/photos/?min_height=&image_type=photo&cat=animals&q=%E5%8A%A8%E7%89%A9&min_width=&order=popular"
    page = urllib2.urlopen(url)
    html = page.read()
    image_pins = re.compile(r' href="(.+?)"')
    pins_list = re.findall(image_pins, html)
    a = 1
    p = 1
    i = 0
    page = 1
    last_page = 30
    while (p == 1):
        if ("pagi" in pins_list[i]):
            p = 0
            while(page<=last_page):
                page_url = change_str_pop(pins_list[i],page)
                print page_url
                url_list=read_url(page_url)
                for url in url_list:
                    if  "动物" in url and "玩具" not in url and "男" not in url and "女" not in url and "植物" not in url  and "人" not in url :
                        image = get_image_from_html(url)
                        save_and_push_image(image, a)
                        a = a + 1
                        print url
                page=page+1
        i=i+1
    return HttpResponse(html)

# 读取html里有的图片链接
def read_url(url):
    html = urllib2.urlopen(url).read()
    req = re.compile(r' href="(.+?)"')
    url_list = re.findall(req, html)
    new_list=[]
    for url in url_list:
        if "-" in url and "/zh/" in url:
            u=urllib2.unquote(url)
            url="https://pixabay.com%s" %u
            new_list.append(url)
    return new_list


# 拼装下一页的链接
def change_str_pop(url, p):
    i = len(url)
    url = url[:(i - 1)] + str(p)
    u=urllib2.unquote(url)
    url="https://pixabay.com%s" %u
    return url


# 从图片页面读取图片
def get_image_from_html(url):
    html = urllib2.urlopen(url).read()
    req = re.compile(r'src="(.+?)"')
    imgre_list = re.findall(req, html)
    b = 1
    i = 0
    while (b == 1):
        if "960_720" in imgre_list[i]:
            b = 0
        else:
            i = i + 1
    data = urllib2.urlopen(imgre_list[i]).read()
    file = cStringIO.StringIO(data)
    image = Image.open(file)
    return image


# 保存到本地，并上传到阿里云
def save_and_push_image(image, n):
    f = first_type = "动物"
    s = second_type = "动物"
    image = deal_image.crop_picture(image)
    color = get_color.abs_rgb(image, 1)
    path = "/Users/wufan/python/pixabay/动物/动物/%s_%s_%s.jpg" % (f, s, n)
    image.save(path)
    o = upload_picture_to_oss.push_image(path, first_type, second_type, "jpg", n)
    oss_url = "http://wufan-picture-app.oss-cn-shenzhen.aliyuncs.com/%s" % o
    models.Pixabay.objects.create(first_type=first_type, second_type=second_type, url=path, oss=oss_url, color=color)
