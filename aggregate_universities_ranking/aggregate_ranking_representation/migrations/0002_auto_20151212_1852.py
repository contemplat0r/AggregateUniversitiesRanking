# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aggregate_ranking_representation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rankingdescription',
            name='year',
            field=models.IntegerField(),
        ),
    ]
