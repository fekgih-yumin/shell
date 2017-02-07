# coding=utf-8
# 这个文件专用于处理图像
import sys
from PIL import Image, ImageFont, ImageDraw
from app import get_color
from app import models
from app import text_image
import time
from app import upload_picture_to_oss


# 裁剪主图
def crop_picture(image, i):
    x, y = image.size

    newimage = image
    if x > y:
        xsize = ysize = y
        ox = (x - y) / 2
        oy = 0
        b = (ox, oy, xsize + ox, ysize)
        newimage = image.crop(b)
    if x <= y:
        xsize = ysize = x
        ox = 0
        oy = (y - ysize) / 2
        b = (ox, oy, xsize, ysize + oy)
        newimage = image.crop(b)
    nx, ny = newimage.size
    print nx, ny
    if (nx % i != 0):
        nx = nx - nx % i
    if (ny % i != 0):
        ny = ny - ny % i
    newimage.thumbnail((nx, ny), Image.ANTIALIAS)
    return newimage


# 根据用户选中的位置切图
def crop_by_customer(image, origin, end, i,size):
    print origin
    print end
    o_point = origin.split('_')
    e_point = end.split('_')
    b = (int(o_point[0]), int(o_point[1]), int(e_point[0]), int(e_point[1]))
    print b
    newimage = image.crop(b)
    newimage = newimage.resize(size, Image.ANTIALIAS)

    nx, ny = newimage.size
    print nx, ny
    if (nx % i != 0):
        nx = nx - nx % i
    if (ny % i != 0):
        ny = ny - ny % i
    newimage.thumbnail((nx, ny), Image.ANTIALIAS)
    return newimage


# 用数据库中色值最接近的图片替换
def draw_picture(image, s, type):
    s = int(s)
    new_xsize, new_ysize = image.size
    ax = new_xsize / s
    ay = new_ysize / s
    size = (ax, ay)
    # 根据类目获取数据库的图片
    photo_list = models.Pixabay.objects.filter(second_type=type)

    # 获取矩阵
    matrix = [None] * (s * s)
    for i in range(len(matrix)):
        matrix[i] = [0] * 4

    k = h = 0  # k是矩阵数，h是每一列的数
    # 迭代每个矩阵
    while (k < (s * s)):
        j = 0  # j是每一列的数
        while (j < s):
            matrix[k + j][0] = ax * h
            matrix[k + j][2] = ax * (h + 1)
            matrix[k + j][1] = ay * j
            matrix[k + j][3] = ay * (j + 1)
            b = (matrix[k + j][0], matrix[k + j][1], matrix[k + j][2], matrix[k + j][3])
            d = (matrix[k + j][0], matrix[k + j][1])
            j = j + 1
            newimage = image.crop(b)  # 裁剪相应大小
            color = get_color.abs_rgb(newimage, 1)
            newimage = get_color.compare_RGBlist(color, type, photo_list)
            print b
            newimage.thumbnail(size, Image.ANTIALIAS)
            image.paste(newimage, b)
        k = k + s
        h = h + 1
    print s * s
    return image


# 用文字替换图片
def draw_text(image, s, text):
    image = image.convert("RGBA")
    s = int(s)
    l = len(text)
    new_xsize, new_ysize = image.size
    ax = new_xsize / s
    ay = new_ysize / s
    size = (ax, ay)
    # 获取矩阵
    matrix = [None] * (s * s)
    for i in range(len(matrix)):
        matrix[i] = [0] * 4

    k = h = 0  # k是矩阵数，h是每一列的数
    # 迭代每个矩阵
    while (k < (s * s)):
        j = 0  # j是每一列的数
        while (j < s):
            matrix[k + j][0] = ax * h
            matrix[k + j][2] = ax * (h + 1)
            matrix[k + j][1] = ay * j
            matrix[k + j][3] = ay * (j + 1)
            b = (matrix[k + j][0], matrix[k + j][1], matrix[k + j][2], matrix[k + j][3])
            d = (matrix[k + j][0], matrix[k + j][1])
            j = j + 1
            print size
            newimage = image.crop(b)  # 裁剪相应大小
            color = get_color.abs_rgb(newimage, 0)
            # txt = Image.new('RGBA', size, (0, 0, 0, 0))
            txt = Image.new('RGB', size, (255, 255, 255))
            fnt = ImageFont.truetype("/Users/wufan/python/newpicture/simsun/simsun.ttc", 16)
            draw = ImageDraw.Draw(txt)
            if (l == 1):
                if (j <= s):
                    draw.text((0, 0), text[0], color, font=fnt)
            if (l == 2):
                if (j < s / l):
                    draw.text((0, 0), text[0], color, font=fnt)
                if (s / l <= j <= s):
                    draw.text((0, 0), text[1], color, font=fnt)

            if (l == 3):
                if (j < s / l):
                    draw.text((0, 0), text[0], color, font=fnt)
                if (s / l <= j < s / l * 2):
                    draw.text((0, 0), text[1], color, font=fnt)
                if (s / l * 2 <= j <= s):
                    draw.text((0, 0), text[2], color, font=fnt)
            if (l == 4):
                if (j < s / l):
                    draw.text((0, 0), text[0], color, font=fnt)
                if (s / l <= j < s / l * 2):
                    draw.text((0, 0), text[1], color, font=fnt)
                if (s / l * 2 <= j < s / l * 3):
                    draw.text((0, 0), text[2], color, font=fnt)
                if (s / l * 3 <= j <= s):
                    draw.text((0, 0), text[3], color, font=fnt)
            if (l == 5):
                if (j < s / l):
                    draw.text((0, 0), text[0], color, font=fnt)
                if (s / l <= j < s / l * 2):
                    draw.text((0, 0), text[1], color, font=fnt)
                if (s / l * 2 <= j < s / l * 3):
                    draw.text((0, 0), text[2], color, font=fnt)
                if (s / l * 3 <= j < s / l * 4):
                    draw.text((0, 0), text[3], color, font=fnt)
                if (s / l * 4 <= j <= s):
                    draw.text((0, 0), text[4], color, font=fnt)
            if (l == 6):
                if (j < s / l):
                    draw.text((0, 0), text[0], color, font=fnt)
                if (s / l <= j < s / l * 2):
                    draw.text((0, 0), text[1], color, font=fnt)
                if (s / l * 2 <= j < s / l * 3):
                    draw.text((0, 0), text[2], color, font=fnt)
                if (s / l * 3 <= j < s / l * 4):
                    draw.text((0, 0), text[3], color, font=fnt)
                if (s / l * 4 <= j < s / l * 5):
                    draw.text((0, 0), text[4], color, font=fnt)
                if (s / l * 5 <= j <= s):
                    draw.text((0, 0), text[5], color, font=fnt)
            if (l == 7):
                if (j < s / l):
                    draw.text((0, 0), text[0], color, font=fnt)
                if (s / l <= j < s / l * 2):
                    draw.text((0, 0), text[1], color, font=fnt)
                if (s / l * 2 <= j < s / l * 3):
                    draw.text((0, 0), text[2], color, font=fnt)
                if (s / l * 3 <= j < s / l * 4):
                    draw.text((0, 0), text[3], color, font=fnt)
                if (s / l * 4 <= j < s / l * 5):
                    draw.text((0, 0), text[4], color, font=fnt)
                if (s / l * 5 <= j < s / l * 6):
                    draw.text((0, 0), text[5], color, font=fnt)
                if (s / l * 6 <= j <= s):
                    draw.text((0, 0), text[6], color, font=fnt)
            if (l == 8):
                if (j < s / l):
                    draw.text((0, 0), text[0], color, font=fnt)
                if (s / l <= j < s / l * 2):
                    draw.text((0, 0), text[1], color, font=fnt)
                if (s / l * 2 <= j < s / l * 3):
                    draw.text((0, 0), text[2], color, font=fnt)
                if (s / l * 3 <= j < s / l * 4):
                    draw.text((0, 0), text[3], color, font=fnt)
                if (s / l * 4 <= j < s / l * 5):
                    draw.text((0, 0), text[4], color, font=fnt)
                if (s / l * 5 <= j < s / l * 6):
                    draw.text((0, 0), text[5], color, font=fnt)
                if (s / l * 6 <= j < s / l * 7):
                    draw.text((0, 0), text[6], color, font=fnt)
                if (s / l * 7 <= j <= s):
                    draw.text((0, 0), text[7], color, font=fnt)
            if (l == 9):
                if (j < s / l):
                    draw.text((0, 0), text[0], color, font=fnt)
                if (s / l <= j < s / l * 2):
                    draw.text((0, 0), text[1], color, font=fnt)
                if (s / l * 2 <= j < s / l * 3):
                    draw.text((0, 0), text[2], color, font=fnt)
                if (s / l * 3 <= j < s / l * 4):
                    draw.text((0, 0), text[3], color, font=fnt)
                if (s / l * 4 <= j < s / l * 5):
                    draw.text((0, 0), text[4], color, font=fnt)
                if (s / l * 5 <= j < s / l * 6):
                    draw.text((0, 0), text[5], color, font=fnt)
                if (s / l * 6 <= j < s / l * 7):
                    draw.text((0, 0), text[6], color, font=fnt)
                if (s / l * 7 <= j < s / l * 8):
                    draw.text((0, 0), text[7], color, font=fnt)
                if (s / l * 8 <= j <= s):
                    draw.text((0, 0), text[8], color, font=fnt)
            if (l == 10):
                if (j < s / l):
                    draw.text((0, 0), text[0], color, font=fnt)
                if (s / l <= j < s / l * 2):
                    draw.text((0, 0), text[1], color, font=fnt)
                if (s / l * 2 <= j < s / l * 3):
                    draw.text((0, 0), text[2], color, font=fnt)
                if (s / l * 3 <= j < s / l * 4):
                    draw.text((0, 0), text[3], color, font=fnt)
                if (s / l * 4 <= j < s / l * 5):
                    draw.text((0, 0), text[4], color, font=fnt)
                if (s / l * 5 <= j < s / l * 6):
                    draw.text((0, 0), text[5], color, font=fnt)
                if (s / l * 6 <= j < s / l * 7):
                    draw.text((0, 0), text[6], color, font=fnt)
                if (s / l * 7 <= j < s / l * 8):
                    draw.text((0, 0), text[7], color, font=fnt)
                if (s / l * 8 <= j < s / l * 9):
                    draw.text((0, 0), text[8], color, font=fnt)
                if (s / l * 9 <= j <= s):
                    draw.text((0, 0), text[9], color, font=fnt)


            # newimage = Image.alpha_composite(newimage, txt)
            # color=get_color.abs_rgb(newimage,1)
            # newimage=get_color.compare_RGBlist(color,type,photo_list)
            image.paste(txt, b)
        k = k + s
        h = h + 1
    print s * s
    return image

# 用数据库中图片半透明拼装
def transparent_image(image, s, type):
    s = int(s)
    new_xsize, new_ysize = image.size
    ax = new_xsize / s
    ay = new_ysize / s
    size = (ax, ay)
    # 根据类目获取数据库的图片
    photo_list = models.Pixabay.objects.filter(second_type=type)

    # 获取矩阵
    matrix = [None] * (s * s)
    for i in range(len(matrix)):
        matrix[i] = [0] * 4

    k = h = 0  # k是矩阵数，h是每一列的数
    # 迭代每个矩阵
    image=image.convert("RGBA")
    R,G,B,A=image.split()
    while (k < (s * s)):
        j = 0  # j是每一列的数
        while (j < s):
            matrix[k + j][0] = ax * h
            matrix[k + j][2] = ax * (h + 1)
            matrix[k + j][1] = ay * j
            matrix[k + j][3] = ay * (j + 1)
            b = (matrix[k + j][0], matrix[k + j][1], matrix[k + j][2], matrix[k + j][3])
            d = (matrix[k + j][0], matrix[k + j][1])
            j = j + 1
            newimage = image.crop(b)  # 裁剪相应大小
            color = get_color.abs_rgb(newimage, 1)
            new_im = get_color.compare_RGBlist(color, type, photo_list)
            new_im.thumbnail(size,Image.ANTIALIAS)
            # txt = Image.new('RGBA', size, (0, 0, 0, 100))
            # txt=new_im.convert('RGBA')
            # newimage = Image.alpha_composite(newimage, txt)
            # new_im=transparent(new_im)
            newimage=newimage.convert("RGBA")
            new_im=new_im.convert("L")
            print newimage.mode
            print new_im.mode
            newimage.putalpha(new_im)
            print b
            # newimage.thumbnail(size, Image.ANTIALIAS)
            image.paste(newimage, b)
        k = k + s
        h = h + 1
    print s * s
    return image


def transparent(im):
    transparent_area = (50,80,100,200)
    transparent=100  #用来调透明度，具体可以自己试
    mask=Image.new('L', im.size, color=transparent)
    draw=ImageDraw.Draw(mask)
    draw.rectangle(transparent_area, fill=0)
    im.putalpha(mask)
    return im