# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregate_ranking_representation', '0002_auto_20151212_1852'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('key', models.CharField(max_length=64, unique=True, serialize=False, primary_key=True)),
                ('value', models.BinaryField()),
            ],
        ),
    ]
