# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-08-01 12:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_address_a_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='a_name',
            field=models.CharField(default='summer', max_length=64),
        ),
    ]
