# coding=utf-8
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Customer(models.Model):
    url = models.CharField('地址', max_length=256)


class Photo(models.Model):
    first_type = models.CharField('第一分类', max_length=256)
    second_type = models.CharField('第二分类', max_length=256)
    url = models.CharField('地址', max_length=256)
    color = models.CharField('色值', max_length=256)
    oss=models.CharField('oss的地址',max_length=256)

class Pixabay(models.Model):
    first_type = models.CharField('第一分类', max_length=256)
    second_type = models.CharField('第二分类', max_length=256)
    url = models.CharField('地址', max_length=256)
    color = models.CharField('色值', max_length=256)
    oss = models.CharField('oss的地址', max_length=256)

class Pixabay_Raw(models.Model):
    first_type = models.CharField('第一分类', max_length=256)
    second_type = models.CharField('第二分类', max_length=256)
    url = models.CharField('地址', max_length=256)
    color = models.CharField('色值', max_length=256)
    oss = models.CharField('oss的地址', max_length=256)
