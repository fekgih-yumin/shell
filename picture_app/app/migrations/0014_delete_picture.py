# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-16 03:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_pixabay_raw'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Picture',
        ),
    ]