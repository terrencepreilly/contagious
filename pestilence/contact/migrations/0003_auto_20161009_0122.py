# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-09 01:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_auto_20161009_0119'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='end',
            field=models.DateTimeField(default=None, help_text='The recorded end of an uninterrupted period of contact between two users.'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='start',
            field=models.DateTimeField(default=None, help_text='The recorded start of an uninterrupted period of contact between two users.'),
        ),
    ]
