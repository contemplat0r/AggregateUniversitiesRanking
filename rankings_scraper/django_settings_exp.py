import os
import sys
from os.path import abspath, join, dirname

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

print os.path.dirname(__file__)
print os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print join(abspath(join(dirname(__file__), '..')), 'aggregate_universities_ranking')

DJANGO_PROJECT_DIR = join(abspath(join(dirname(__file__), '..')), 'aggregate_universities_ranking')
sys.path.append(DJANGO_PROJECT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aggregate_universities_ranking.settings')
import django
django.setup()
from aggregate_ranking_representation.models import RankingName, RawRankingRecord

ranking_name_list = RankingName.objects.filter(short_name='QS')
print ranking_name_list
ranking_name = ranking_name_list[0]
all_raw_ranking_record = ranking_name.rawrankingrecord_set.all()
print all_raw_ranking_record
ranking_name.rawrankingrecord_set.create(university_name='MIT', country='US', original_value='1', number_in_ranking_table=1)
raw_ranking_record = RawRankingRecord.objects.filter(number_in_ranking_table=1)[0]
print raw_ranking_record
print 'delete: ', raw_ranking_record.delete()
print RawRankingRecord.objects.all()
