# coding=utf-8
# 用于处理文字后，加入图片
from PIL import Image,ImageDraw,ImageFont


def deal_image(size,color):
    text=u"你"
    font = ImageFont.truetype('/Users/wufan/python/newpicture/simsun/simsun.ttc', 10)
    im = Image.new("RGB", size, (255, 255, 255))
    draw = ImageDraw.Draw(im)
    try:
        draw.text((0,0), text, color, font=font)
    except:
        print "draw error"
    return im
