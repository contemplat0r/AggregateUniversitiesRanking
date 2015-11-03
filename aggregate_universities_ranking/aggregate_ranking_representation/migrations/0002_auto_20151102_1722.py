# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregate_ranking_representation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RankingName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_name', models.CharField(max_length=20)),
                ('full_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='RankingValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.DateField()),
                ('original_value', models.CharField(max_length=16)),
                ('number_in_ranking_table', models.IntegerField()),
                ('aggregate_ranking', models.IntegerField(null=True, blank=True)),
                ('ranking_name', models.ForeignKey(to='aggregate_ranking_representation.RankingName')),
            ],
        ),
        migrations.CreateModel(
            name='RawRankingRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('university_name', models.CharField(max_length=512)),
                ('country', models.CharField(max_length=64, null=True, blank=True)),
                ('original_value', models.CharField(max_length=16)),
                ('number_in_ranking_table', models.IntegerField()),
                ('ranking_name', models.ForeignKey(to='aggregate_ranking_representation.RankingName')),
            ],
        ),
        migrations.RemoveField(
            model_name='raitingname',
            name='university',
        ),
        migrations.RemoveField(
            model_name='raitingvalue',
            name='raiting_name',
        ),
        migrations.RemoveField(
            model_name='raitingvalue',
            name='university_name',
        ),
        migrations.AddField(
            model_name='universityname',
            name='country',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
        migrations.DeleteModel(
            name='RaitingName',
        ),
        migrations.DeleteModel(
            name='RaitingValue',
        ),
        migrations.AddField(
            model_name='rankingvalue',
            name='university_name',
            field=models.ForeignKey(to='aggregate_ranking_representation.UniversityName'),
        ),
        migrations.AddField(
            model_name='rankingname',
            name='university',
            field=models.ManyToManyField(to='aggregate_ranking_representation.UniversityName', through='aggregate_ranking_representation.RankingValue'),
        ),
    ]
