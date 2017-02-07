# coding=utf-8
# 用于色值处理和各种方式读取色值
import colorsys
from app import models
from PIL import Image
import urllib2
import cStringIO


# 分别取出r,g,b
def get_list(rgb):
    rgb_list=rgb.split(',')
    r=int(rgb_list[0])
    g=int(rgb_list[1])
    b=int(rgb_list[2])
    return r,g,b

# 读出图片的平均rgb
def abs_rgb(image,t):
    # file="/tmp/newpictures/P00001_0000001.jpg"
    # image=Image.open(file)
    image=image.convert("RGB")
    wigth,higth=image.size
    R=0
    G=0
    B=0
    i=0
    pix=image.load()
    for x in range(wigth):
        for y in range(higth):
            r,g,b=pix[x,y]
            R=R+r
            G=G+g
            B=B+b
            i=i+1
    R=R/i
    G=G/i
    B=B/i
    print R,G,B
    if t==0:
        RGB=(R,G,B)
    if t==1:
        RGB = '%s,%s,%s' % (R, G, B)
    return RGB

# 读出主色值
def get_dominant_color(file, t):
    print type(file)
    image = file.convert('RGBA')
    image.thumbnail((200, 200))
    max_score = None
    dominant_color = None
    for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
        # 跳过黑色
        if a == 0:
            continue

        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
        y = (y - 16.0) / (235 - 16)
        # 跳过亮光部分
        if y > 0.9:
            continue

        score = (saturation + 0.1) * count
        if score > max_score:
            max_score = score
            if t == 0:
                dominant_color = (r, g, b)
            if t == 1:
                dominant_color = '%s,%s,%s' % (r, g, b)
    return dominant_color


# 将RGB三个值分别相减取绝对值，再比较绝对值
def compare_RGBlist(rgb,type,photo_list):
    r,g,b=get_list(rgb)
    if hasattr(photo_list[0],"color"):
        RGB=getattr(photo_list[0],"color")
        R,G,B=get_list(RGB)
        d=abs(r-R)+abs(g-G)+abs(b-B)
        print d

    for photo in photo_list:
        if hasattr(photo,"color"):
            RGB=getattr(photo,"color")
            R,G,B=get_list(RGB)
            a=abs(r-R)+abs(g-G)+abs(b-B)
            if(a<=d):
                d=a
                oss_url=getattr(photo,"oss")
                # tmp_url=getattr(photo,"url")
                color=getattr(photo,"color")
    # image=Image.open(tmp_url)
    image=get_image_from_url(oss_url)
    print color
    return image

def get_image_from_url(url):
    url_list=url.split("http://wufan-picture-app.oss-cn-shenzhen.aliyuncs.com/")
    last= url_list[1]
    last=last.encode('utf-8')
    url="http://wufan-picture-app.oss-cn-shenzhen.aliyuncs.com/%s" %last
    print url
    data=urllib2.urlopen(url).read()
    file=cStringIO.StringIO(data)
    image=Image.open(file)
    return image