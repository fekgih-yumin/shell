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

def get_images(request):
    url="http://huaban.com/boards/16158239/"
    page=urllib2.urlopen(url)
    html=page.read()
    image_pins=re.compile(r' href="/pins/(.+?)"')
    pins_list=re.findall(image_pins,html)
    # print pins_list
    b=first_type="花卉"
    c=second_type="玫瑰"
    a=80
    for p in pins_list:
        if len(p)>6:
            image_url = "http://huaban.com/pins/%s" % p
            print image_url
            im=get_image(image_url)
            if im=="":
                print "----------------------------------------------------------"
            else:

                t = im.format
                if t=="JPG" or t=="JPEG":
                    local_path = "/Users/wufan/python/images/花卉/玫瑰/%s_%s%s.jpeg" % (b,c,a)
                    im.save(local_path)
                    color = get_color.abs_rgb(im, 1)  # 读出图片的平均色值rgb
                    # color = views.get_dominant_color(im,1)
                    print local_path
                    try:
                        o = upload_picture_to_oss.push_image(local_path, first_type, second_type,im.format,a)
                        oss_url = "http://app-pictures.oss-cn-shenzhen.aliyuncs.com/%s" % o
                    except:
                        print "上传失败"
                        # print "oss的地址是：%s" %
                    try:
                        models.Photo.objects.create(first_type=first_type, second_type=second_type, url=local_path,
                                                    oss=oss_url, color=color)
                    except:
                        print "保存数据库失败"

            a = a + 1
    return HttpResponse(html)

def get_image(url):
    page=urllib2.urlopen(url)
    html=page.read()
    imgre=re.compile(r' src="(.+?)"')
    image_list=re.findall(imgre,html)
    wigth=501
    a=1
    for i in image_list:
        if ("fw658" in i) and (wigth>300) and(a==1):
            # print i
            image_url="http:%s" %i
            data = urllib2.urlopen(image_url).read()
            image = cStringIO.StringIO(data)
            im = Image.open(image)
            x, y = im.size
            # if x > wigth :
            # print image_url
            wigth == 0
            a=0
    return im

