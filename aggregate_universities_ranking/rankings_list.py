from name_matching import *

rankings = RankingName.objects.all()

rankings_list = [{'short_name' : ranking.short_name, 'full_name' : ranking.full_name, 'url' : str(), 'year' : 2015} for ranking in list(rankings)]
print rankings_list
