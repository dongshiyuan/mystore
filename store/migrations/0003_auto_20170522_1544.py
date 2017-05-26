# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-05-22 15:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20170522_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='sex',
            field=models.CharField(choices=[('m', '男'), ('w', '女')], default='m', max_length=2, verbose_name='性别'),
        ),
    ]