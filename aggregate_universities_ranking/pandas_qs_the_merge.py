# coding: utf-8

from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import django
django.setup()
from aggregate_ranking_representation.models import RankingName, RawRankingRecord
qs_name = RankingName.objects.filter(short_name='QS')[0]
the_name = RankingName.objects.filter(short_name='THE')[0]
qs_raw_records = list(qs_name.rawrankingrecord_set.all().values())
the_raw_records = list(the_name.rawrankingrecord_set.all().values())
qs_df = DataFrame(qs_raw_records)
the_df = DataFrame(the_raw_records)
qs_df[:3]
the_df[:3)
the_df[:3]
the_df.drop(0, axis=0)
the_df = the_df.drop(0, axis=0)
the_df
the_df[:3]
f = lambda x: x - 1
the_df['number_in_ranking_table'] = the_df['number_in_ranking_table'].map(f)
the_df[:3]
qs_short_df = qs_df[['number_in_ranking_table', 'university_name', 'country']]
qs_short_df[:3]
the_short_df = the_df[['number_in_ranking_table', 'university_name', 'country']]
qs_the_outer_merge = pd.merge(qs_short_df, the_short_df, on='university_name', how='outer', suffixes=('_qs', '_the'))
qs_the_outer_merge[qs_the_outer_merge['number_in_ranking_table_qs'].isnull() | qs_the_outer_merge['number_in_ranking_table_the'].isnull()]
qs_the_outer_merge_na = qs_the_outer_merge[qs_the_outer_merge['number_in_ranking_table_qs'].isnull() | qs_the_outer_merge['number_in_ranking_table_the'].isnull()]
qs_the_outer_merge_na[:3]
qs_the_outer_merge_na[:10]
len(qs_the_outer_merge_na[:10])
len(qs_the_outer_merge_na)
qs_the_outer_merge_not_na = qs_the_outer_merge[(qs_the_outer_merge['country_qs'] != np.na) & (qs_the_outer_merge['country_the'] != np.na)]
get_ipython().magic(u'pinfo np.logical_and')
qs_the_outer_merge_not_na = qs_the_outer_merge[(qs_the_outer_merge['country_qs'] != np.nan) & (qs_the_outer_merge['country_the'] != np.nan)]
len(qs_the_outer_merge_not_na)
qs_the_outer_merge.count
qs_the_outer_merge.count()
qs_the_outer_merge_na.count()
1326 -933
qs_the_inner_merge = pd.merge(qs_short_df, the_short_df, on='university_name', how='inner', suffixes=('_qs', '_the'))
qs_the_inner_merge.count
1326 -933
qs_the_inner_merge.count()
