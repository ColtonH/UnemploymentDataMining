# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_auto_20141011_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='usstate',
            name='code',
            field=models.CharField(default='', max_length=2),
            preserve_default=False,
        ),
    ]
