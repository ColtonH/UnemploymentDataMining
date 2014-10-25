# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnemploymentByStateMonthly',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.PositiveIntegerField()),
                ('month', models.PositiveIntegerField()),
                ('value', models.FloatField()),
                ('state', models.ForeignKey(to='data.UsState')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='unemploymentbystate',
            name='state',
        ),
        migrations.DeleteModel(
            name='UnemploymentByState',
        ),
    ]
