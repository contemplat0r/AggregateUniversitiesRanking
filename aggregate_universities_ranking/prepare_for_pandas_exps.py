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
leiden_name = RankingName.objects.filter(short_name='Leiden')[0]
leiden_raw_records = list(leiden_name.rawrankingrecord_set.all().values())
leiden_df = DataFrame(leiden_raw_records)

the_df = the_df.drop(0, axis=0)
#f = lambda x: x - 1
#the_df['number_in_ranking_table'] = the_df['number_in_ranking_table'].map(f)

the_df['number_in_ranking_table'] = the_df['number_in_ranking_table'].map(lambda x: x -1 ) 

qs_short_df = qs_df[['number_in_ranking_table', 'university_name', 'country']]
the_short_df = the_df[['number_in_ranking_table', 'university_name', 'country']]

qs_the_outer_merge = pd.merge(qs_short_df, the_short_df, on='university_name', how='outer', suffixes=('_qs', '_the'))

qs_the_outer_merge_na = qs_the_outer_merge[qs_the_outer_merge['number_in_ranking_table_qs'].isnull() | qs_the_outer_merge['number_in_ranking_table_the'].isnull()]
qs_the_outer_merge_not_na = qs_the_outer_merge[(qs_the_outer_merge['country_qs'] != np.nan) & (qs_the_outer_merge['country_the'] != np.nan)]

qs_the_inner_merge = pd.merge(qs_short_df, the_short_df, on='university_name', how='inner', suffixes=('_qs', '_the'))
print 'len(qs_the_outer_merge_na): ', len(qs_the_outer_merge_na)
print 'qs_the_outer_merge.count(): ', qs_the_outer_merge.count()
print 'qs_the_outer_merge_na.count(): ',  qs_the_outer_merge_na.count()
print 'qs_the_inner_merge.count(): ', qs_the_inner_merge.count()
