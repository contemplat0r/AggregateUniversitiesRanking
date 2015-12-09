from name_matching import *

rankings_descriptions_list = [{'url': '', 'full_name': u'QS World University Rankings', 'short_name': u'QS', 'year': 2015}, {'url': '', 'full_name': u'Times Higher Education', 'short_name': u'THE', 'year': 2015}, {'url': '', 'full_name': u'Academic Ranking of World Universities', 'short_name': u'ARWU', 'year': 2015}, {'url': '', 'full_name': u'CWTS Leiden Ranking', 'short_name': u'Leiden', 'year': 2015}, {'url': '', 'full_name': u'National Taiwan University Ranking', 'short_name': u'NTU', 'year': 2015}, {'url': '', 'full_name': u'University Ranking by Academic Performance', 'short_name': u'URAP', 'year': 2015}, {'url': '', 'full_name': u'Webometrics Ranking of World Universities', 'short_name': u'Webometrics', 'year': 2015}]

for ranking_description in rankings_descriptions_list:
    ranking_description_db_record = RankingDescription(short_name=ranking_description['short_name'], full_name=ranking_description['full_name'], url=ranking_description['url'], year=ranking_description['year'])
    ranking_description_db_record.save()
