# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UnemploymentByState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.PositiveIntegerField()),
                ('month', models.PositiveIntegerField()),
                ('value', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='usstate',
            unique_together=set([('name',)]),
        ),
        migrations.AddField(
            model_name='unemploymentbystate',
            name='state',
            field=models.ForeignKey(to='data.UsState'),
            preserve_default=True,
        ),
    ]
