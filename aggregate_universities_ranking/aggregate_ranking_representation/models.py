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

class UniversityName(models.Model):
    university_name = models.CharField(max_length=512)
    country = models.CharField(max_length = 64, null=True, blank=True)
    #url = models.CharField(max_length=200)

    def __str__(self):
        return self.university_name


class RankingName(models.Model):
    #abbreviation = models.CharField(max_length=20, null=True, blank=True)
    short_name = models.CharField(max_length=20)
    full_name = models.CharField(max_length=200)
    #url = models.CharField(max_length=200)
    #length = models.IntegerField()
    #year = models.IntegerField()
    university = models.ManyToManyField(UniversityName, through='RankingValue')

    def __str__(self):
        return self.short_name

class RawRankingRecord(models.Model):
    university_name = models.CharField(max_length=512)
    country = models.CharField(max_length = 64, null=True, blank=True)
    original_value = models.CharField(max_length=16) # Значение приведённое на сайте рейтинга. Может быть и 1, 2...100, а может быть и 601-800 (см. последние записи в THE, и просто "-" (см. последние записи в URAP).
    number_in_ranking_table = models.IntegerField() # Просто номер строки (записи) в таблице рейтинга если считать их (записи) "сверху-вниз" непрерывно прямо на странице (страницах) рейтинга.
    ranking_name = models.ForeignKey(RankingName)
    
    def __str__(self):
        return self.university_name

class RankingValue(models.Model):
    year = models.DateField(auto_now=False, auto_now_add=False)
    original_value = models.CharField(max_length=16) # Значение приведённое на сайте рейтинга. Может быть и 1, 2...100, а может быть и 601-800 (см. последние записи в THE, и просто "-" (см. последние записи в URAP).
    number_in_ranking_table = models.IntegerField() # Просто номер строки (записи) в таблице рейтинга если считать их (записи) "сверху-вниз" непрерывно прямо на странице (страницах) рейтинга. Либо посчитанные моим методом (см. статью) если данного университета в данном рейтинге нет.
    aggregate_ranking = models.IntegerField(null=True, blank=True)
    ranking_name = models.ForeignKey(RankingName)
    university_name = models.ForeignKey(UniversityName)

    def __str__(self):
        return u'Rank: %s, Year: %s' % (str(self.number_in_ranking_table), str(self.year.year))
