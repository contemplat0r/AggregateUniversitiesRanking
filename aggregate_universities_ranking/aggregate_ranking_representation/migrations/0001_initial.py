# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RaitingName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_name', models.CharField(max_length=20)),
                ('full_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='RaitingValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.DateField()),
                ('value', models.CharField(max_length=16)),
                ('number_in_raiting_table', models.IntegerField()),
                ('raiting_name', models.ForeignKey(to='aggregate_ranking_representation.RaitingName')),
            ],
        ),
        migrations.CreateModel(
            name='UniversityName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('university_name', models.CharField(max_length=512)),
            ],
        ),
        migrations.AddField(
            model_name='raitingvalue',
            name='university_name',
            field=models.ForeignKey(to='aggregate_ranking_representation.UniversityName'),
        ),
        migrations.AddField(
            model_name='raitingname',
            name='university',
            field=models.ManyToManyField(to='aggregate_ranking_representation.UniversityName', through='aggregate_ranking_representation.RaitingValue'),
        ),
    ]
