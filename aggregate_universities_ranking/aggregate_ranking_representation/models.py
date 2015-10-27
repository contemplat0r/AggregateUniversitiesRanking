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

    def __str__(self):
        return self.university_name

class RaitingName(models.Model):
    #abbreviation = models.CharField(max_length=20, null=True, blank=True)
    short_name = models.CharField(max_length=20)
    full_name = models.CharField(max_length=200)
    university = models.ManyToManyField(UniversityName, through='RaitingValue')

    def __str__(self):
        return self.short_name

class RaitingValue(models.Model):
    year = models.DateField(auto_now=False, auto_now_add=False)
    value = models.CharField(max_length=16)
    number_in_raiting_table = models.IntegerField()
    raiting_name = models.ForeignKey(RaitingName)
    university_name = models.ForeignKey(UniversityName)
