# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class SearchPhrase(models.Model):
    phrase = models.CharField(max_length=1000)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.phrase

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'SearchPhrase'
        verbose_name_plural = 'SearchPhrases'


class Tweet(models.Model):
    search_phrase = models.ForeignKey(SearchPhrase, related_name='tweet_set', on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    user = models.CharField(max_length=255)
    post = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.post)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Tweet'
        verbose_name_plural = 'Tweets'