# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RankingDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_name', models.CharField(max_length=20)),
                ('full_name', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=200, null=True, blank=True)),
                ('original_ranking_length', models.IntegerField(null=True, blank=True)),
                ('year', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='RankingValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original_value', models.CharField(max_length=16)),
                ('number_in_ranking_table', models.IntegerField()),
                ('ranking_description', models.ForeignKey(to='aggregate_ranking_representation.RankingDescription')),
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
                ('ranking_description', models.ForeignKey(to='aggregate_ranking_representation.RankingDescription')),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('university_name', models.CharField(unique=True, max_length=512)),
                ('country', models.CharField(max_length=64, null=True, blank=True)),
                ('url', models.CharField(max_length=200, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='rankingvalue',
            name='university',
            field=models.ForeignKey(to='aggregate_ranking_representation.University'),
        ),
        migrations.AddField(
            model_name='rankingdescription',
            name='university',
            field=models.ManyToManyField(to='aggregate_ranking_representation.University', through='aggregate_ranking_representation.RankingValue'),
        ),
        migrations.AlterUniqueTogether(
            name='rankingdescription',
            unique_together=set([('short_name', 'year')]),
        ),
    ]
