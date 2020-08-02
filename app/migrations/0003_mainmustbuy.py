# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-05-02 10:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_mainnav'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainMustbuy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=50)),
                ('trackid', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'axf_mustbuy',
            },
        ),
    ]
