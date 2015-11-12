# coding: utf-8

import django
import django_pandas
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
django.setup()
from aggregate_ranking_representation.models import RawRankingRecord, RankingName
qs_name = RankingName.objects.filter(short_name='QS')[0]
the_name = RankingName.objects.filter(short_name='THE')[0]
leiden_name = RankingName.objects.filter(short_name='Leiden')[0]
qs_raw_records = qs_name.rawrankingrecord_set.all().values()
qs_raw_records = list(qs_name.rawrankingrecord_set.all().values())
the_raw_records = list(the_name.rawrankingrecord_set.all().values())
leiden_raw_records = list(leiden_name.rawrankingrecord_set.all().values())
len(qs_raw_records)
len(the_raw_records)
len(leiden_raw_records)
qs_df = DataFrame(qs_raw_records)
the_df = DataFrame(the_raw_records)
leiden_df = DataFrame(leiden_raw_records)
the_df.head()
the_df = the_df.drop(0, axis=0)
the_df.head()
f = lambda x: x - 1
the_df['number_in_ranking_table'] = the_df['number_in_ranking_table'].map(f)
the_df.head()
qs_names_df = the_df[['university_name', 'country']]
qs_names_df.head()
qs_names_df = qs_df[['university_name', 'country']]
the_names_df = the_df[['university_name', 'country']]
leiden_names_df = leiden_df[['university_name', 'country']]
leiden_names_df.head()
qs_the_names_df = pd.merge(qs_names_df, the_names_df, on='university_name', how='inner', suffixes=('_qs', '_the'))
qs_the_names_df
qs_the_names_df[:5]
qs_the_names_df_inner = pd.merge(qs_names_df, the_names_df, on='university_name', how='inner', suffixes=('_qs', '_the'))
qs_the_names_df_outer = pd.merge(qs_names_df, the_names_df, on='university_name', how='outer', suffixes=('_qs', '_the'))
qs_the_names_df_outer[:5]
qs_the_names_df_outer['country_qs' == NaN & 'country_the' == NaN]
qs_the_names_df_outer['country_qs' ==  & 'country_the' == NaN]
qs_the_names_df_outer['country_qs' == np.nan  & 'country_the' == np.nan]
qs_the_names_df_outer['country_qs' == np.nan]
qs_the_names_df_outer[['country_qs' == np.nan]]
qs_the_names_df_outer['country_qs'] = np.nan
qs_the_names_df_outer = pd.merge(qs_names_df, the_names_df, on='university_name', how='outer', suffixes=('_qs', '_the'))
qs_the_names_df_outer['country_qs'] == np.nan
qs_the_names_df_outer['country_qs'] == np.nan|less
qs_the_names_df_outer['country_the'] == np.nan
qs_the_names_df_outer[:5]
qs_the_names_df_outer[:20]
qs_the_names_df_right = pd.merge(qs_names_df, the_names_df, on='university_name', how='right', suffixes=('_qs', '_the'))
qs_the_names_df_right[:20]
qs_the_names_df_right
qs_the_names_df_left = pd.merge(qs_names_df, the_names_df, on='university_name', how='left', suffixes=('_qs', '_the'))
qs_the_names_df_left
