# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-10 07:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0005_delete_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_type', models.CharField(max_length=256, verbose_name='\u7b2c\u4e00\u5206\u7c7b')),
                ('second_type', models.CharField(max_length=256, verbose_name='\u7b2c\u4e8c\u5206\u7c7b')),
                ('url', models.CharField(max_length=256, verbose_name='\u5730\u5740')),
                ('color', models.CharField(max_length=256, verbose_name='\u8272\u503c')),
                ('oss', models.CharField(max_length=256, verbose_name='oss\u7684\u5730\u5740')),
            ],
        ),
    ]
