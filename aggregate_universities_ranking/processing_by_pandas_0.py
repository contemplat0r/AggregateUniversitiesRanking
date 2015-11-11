# coding: utf-8

import django
django.setup()
from aggregate_ranking_representation.models import RankingName, RawRankingRecord
qs_name = RankingName.objects.filter(short_name='QS')
qs_name = RankingName.objects.filter(short_name='QS')[0]
the_name = RankingName.objects.filter(short_name='THE')[0]
from aggregate_ranking_representation.models import RawRankingRecord, RankingName
from pandas import Series, DataFrame
import pandas as pd
qs_raw_records = qs_name.rawrankingrecord_set.all()
qs_raw_records
qs_raw_record0 = qs_raw_records[0]
qs_raw_record0
qs_raw_records = qs_name.rawrankingrecord_set.all().values()
qs_raw_records
qs_df = DataFrame(qs_raw_records)
qs_df = DataFrame(list(qs_raw_records))
qs_df.head()
the_name = RankingName.objects.filter(short_name='THE')
the_name = RankingName.objects.filter(short_name='THE')[0]
the_raw_records = the_name.rawrankingrecord_set.all()
the_df = DataFrame(list(the_raw_records.values()))
the_df.head()
the_df[:-1]
the_df.index
the_df.drop(0, axis=0)
the_df.head()
the_df.drop(0)
the_df.head()
the_df = DataFrame(list(the_raw_records.values()))
the_df.head()
the_df[0]
the_df[1]
the_df.last
the_df = DataFrame(list(the_raw_records.values()))
the_df.last
del the_df
the_df = DataFrame(list(the_raw_records.values()))
the_df.last
the_df[:10]
the_df.index
the_df.shape
the_df.axes
the_df.axes.index
the_df.axes.index()
get_ipython().magic(u'pinfo the_df.axes.index')
the_df_drop0 = the_df.drop(0)
the_df_drop0.head()
f = lambda x: x - 1
the_df_drop0['number_in_ranking_table'].map(f)
the_df_drop0
the_df_drop0.head()
the_df_drop0['number_in_ranking_table'] = the_df_drop0['number_in_ranking_table'].map(f)
the_df_drop0.head()
the_df_drop0
the_df = the_df.drop(0, axis=0)
the_df.head()
the_df['number_in_ranking_table'] = the_df['number_in_ranking_table'].map(f)
the_df.head()
qs_the_inner_merge = pd.merge(qs_df, the_df, on='university_name', how='inner', suffixes=('_qs', '_the'))
qs_the_inner_merge.head()
qs_the_inner_merge
qs_the_inner_merge[['university_name', 'number_in_ranking_table_qs', 'number_in_ranking_table_the']][:20]
qs_the_inner_merge[['university_name', 'number_in_ranking_table_qs', 'number_in_ranking_table_the', 'country_qs', 'country_the']][:20]
qs_the_outer_merge = pd.merge(qs_df, the_df, on='university_name', how='outer', suffixes=('_qs', '_the'))
qs_the_outer_merge
