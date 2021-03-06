# -*- coding: utf8 -*- 

from django.db import models

# Create your models here.

# Как минимум три модели: 1) названия рейтингов, 2) названия университетов, 3) само значение рейтига данного университета в данном рейтинге.
# Очевидно, что что модели 1 и 2 связаны отношением "многие ко многим" посредством модели 3, так как один и тот же университет может входить в различные рейтинги (а может и не входить), а, данный рейтинг может включать (а может и не включать) в себя различные университеты.

# Структуры таблиц:
# 1. "Названия Рейтингов" - название рейтинга и, может быть дату (кого, чего дату?).
# 2. "Университеты" - название университета (всю работу с названиями "сбрасываем" на нативные средства Python, Pandas, NLTK. Может быть дату (кого, чего?)
# "Значение рейтинга" - значение рейтинга (там уже в зависимости от той таблицы из которой берётся) и здесь уже точно год к которому относиться данное значение. Можно дату записи в таблицу.
# Названия таблиц определились сами собой: 1) RaitingName, 2) UniversityName, 3) RaitingValue.


class University(models.Model):
    university_name = models.CharField(max_length=512, unique=True)
    country = models.CharField(max_length = 64, null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.university_name


class RankingDescription(models.Model):
    short_name = models.CharField(max_length=20)
    full_name = models.CharField(max_length=200)
    url = models.CharField(max_length=200, null=True, blank=True)
    original_ranking_length = models.IntegerField(null=True, blank=True)
    #year = models.IntegerField(null=True, blank=True)
    year = models.IntegerField()
    #university = models.ManyToManyField(University, through='RankingValue', null=True, blank=True)
    university = models.ManyToManyField(University, through='RankingValue')

    class Meta:
        unique_together = ('short_name', 'year')
    def __str__(self):
        return '(%s, %s)' % (self.short_name, self.full_name)


class RawRankingRecord(models.Model):
    university_name = models.CharField(max_length=512)
    country = models.CharField(max_length = 64, null=True, blank=True)
    original_value = models.CharField(max_length=16) # Значение приведённое на сайте рейтинга. Может быть и 1, 2...100, а может быть и 601-800 (см. последние записи в THE, и просто "-" (см. последние записи в URAP).
    number_in_ranking_table = models.IntegerField() # Просто номер строки (записи) в таблице рейтинга если считать их (записи) "сверху-вниз" непрерывно прямо на странице (страницах) рейтинга.
    ranking_description = models.ForeignKey(RankingDescription)
    #ranking_name = models.ForeignKey(RankingName)
    
    def __str__(self):
        return self.university_name


class RankingValue(models.Model):
    #year = models.DateField(auto_now=False, auto_now_add=False)
    original_value = models.CharField(max_length=16) # Значение приведённое на сайте рейтинга. Может быть и 1, 2...100, а может быть и 601-800 (см. последние записи в THE, и просто "-" (см. последние записи в URAP).
    number_in_ranking_table = models.IntegerField() # Просто номер строки (записи) в таблице рейтинга если считать их (записи) "сверху-вниз" непрерывно прямо на странице (страницах) рейтинга. Либо посчитанные моим методом (см. статью) если данного университета в данном рейтинге нет.
    #aggregate_ranking = models.IntegerField(null=True, blank=True)
    #ranking_name = models.ForeignKey(RankingName)
    ranking_description = models.ForeignKey(RankingDescription)
    university = models.ForeignKey(University)
    #university_name = models.ForeignKey(UniversityName)

    def __str__(self):
        #return u'Rank: %s, Year: %s' % (str(self.number_in_ranking_table), str(self.year.year))
        return u'Rank: %s' % str(self.number_in_ranking_table)

class Result(models.Model):
    key = models.CharField(max_length=64, null=False, blank=False, primary_key=True, unique=True)
    value = models.TextField()

    def __str__(self):
        return 'Result key: %s' % self.key


#class LangTranslation(models.Model):
#    lang_name = CharField(max_length=2, null=False, blank=False)
#    key = CharField(max_length=32, null, False, blank=False)
#    value = CharField(max_length=64)

class BigSiteText(models.Model):
    lang = models.CharField(max_length=4, null=False, blank=False)
    text_name = models.CharField(max_length=64, null=False, blank=False)
    text = models.TextField()

    def __str__(self):
        return '%s%s' % (self.text_name, self.lang)
