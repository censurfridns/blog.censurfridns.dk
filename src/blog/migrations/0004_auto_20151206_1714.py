# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogpost_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='body_da',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='body_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='title_da',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='title_en',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
