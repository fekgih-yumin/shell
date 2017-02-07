# coding=utf-8
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import time
from app import deal_image
from django.http import HttpResponse
from PIL import Image
import urllib2
import cStringIO
from app import models
import sys
import json
from app import upload_picture_to_oss
from app.models import Photo


@csrf_exempt
def image_to_deal(request):
    t=time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    print t
    print request.FILES
    # i= request.FILES['image'],request.META['HTTP_I']
    file=request.FILES['image']
    i=50
    type=request.GET.get('type')
    origin=request.GET.get('origin')
    end=request.GET.get('end')
    print origin,end

    # end="720_720"
    # type="猫"
    print i
    image=Image.open(file)
    # croped_image=deal_image.crop_picture(image)                         # 裁剪图片
    croped_image=deal_image.crop_by_customer(image,origin,end,i,(3000,3000))            # 裁剪图片
    image=deal_image.draw_picture(croped_image,i,type)                  # 拼装图片
    path = "/Users/wufan/python/dealed_pictures/%s_%s.jpg" % (t, type)  # 保存到本地
    image.save(path)
    o = upload_picture_to_oss.push_image_customer(path, type)           # 上传到oss
    oss_url = "http://wufan-picture-app.oss-cn-shenzhen.aliyuncs.com/%s" % o
    # 保存数据库
    models.Customer.objects.create(url=oss_url)
    return HttpResponse(json.dumps({"oss_url":oss_url},ensure_ascii=False))

@csrf_exempt
def text_deal(request):
    t = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    file=request.FILES['image']
    image=Image.open(file)
    origin=request.GET.get('origin')
    end=request.GET.get('end')
    text=request.GET.get('text')
    print origin ,end,text
    # text="好好学习天上"
    text=unicode(text,"utf-8")
    text=list(text)
    end="720_720"
    i=80
    image=deal_image.crop_by_customer(image,origin,end,i,(1200,1200))
    im=deal_image.draw_text(image,i,text)
    path="/Users/wufan/python/dealed_pictures/%s.jpg" %t
    im.save(path)
    o = upload_picture_to_oss.push_image_customer(path, "text")  # 上传到oss
    oss_url = "http://wufan-picture-app.oss-cn-shenzhen.aliyuncs.com/%s" % o
    # 保存数据库
    models.Customer.objects.create(url=oss_url)
    return HttpResponse(json.dumps({"oss_url":oss_url},ensure_ascii=False))


#查询图片接口
def image_database_images(request):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    second_type=request.GET.get('second_type')
    page=int(request.GET.get('page'))
    print page
    i=20
    if page==None:
        photo_list = models.Pixabay.objects.filter(second_type=second_type)
    else:
        photo_list = models.Pixabay.objects.filter(second_type=second_type)[i*(page-1):page*i-1]
    image_list=[]
    print photo_list
    for photo in photo_list:
        oss_url=getattr(photo,"oss")
        oss_url=urllib2.unquote(oss_url)
        image_list.append(oss_url)
    a={"images":image_list}
    return HttpResponse(json.dumps(a,ensure_ascii=False))



#查询图库类目名
def get_typename(request):
    first_type=request.GET.get('first_type')
    new_types = []
    if first_type==None:
        types=models.Pixabay.objects.values('first_type').distinct()
        print types
        for type in types:
            new_types.append(type["first_type"])
    else:
        type_list=models.Pixabay.objects.filter(first_type=first_type)
        for type in type_list:
            s_type=getattr(type,"second_type")
            if s_type not in new_types:
                new_types.append(s_type)
    # return HttpResponse(json.dumps({"types":types}))
    return HttpResponse(json.dumps({"types":new_types},ensure_ascii=False))

# @csrf_exempt
# def deal_thumb(request):
#     t=time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
#     print t
#     # i= request.FILES['image'],request.META['HTTP_I']
#     file=request.FILES['image']
#     image=Image.open(file)
#     image = deal_image.crop_picture(image)
#     i=20
#     image=deal_image.draw_text(image,i,text="hello")
#     path = "/Users/wufan/python/dealed_pictures/%s.jpeg" % t
#     image.save(path)
#     return HttpResponse("ok", "application/json; charset=utf-8")

@csrf_exempt
def transparent_image(request):
    t = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    file=request.FILES['image']
    image=Image.open(file)
    im=deal_image.transparent_image(image,20,"猫")
    # im=deal_image.transparent(image)
    path = "/Users/wufan/python/dealed_pictures/%s.png" % t
    im.save(path)
    return HttpResponse("ok")