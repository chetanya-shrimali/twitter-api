# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
from requests_oauthlib import OAuth1

from django.shortcuts import render
from api.models import SearchPhrase, Tweet
from datetime import datetime


def index(request):
    # sending request
    search_term = request.GET.get('search_term')
    username = request.GET.get('username')
    date = request.GET.get('date')

    tweets = ''
    message = ''

    if not search_term and not username:
        message = 'Please enter the values to fetch tweet results!'
    else:
        phrase = str(search_term) + ' ' + str(username) + ' ' + str(date) + ' ' + str(datetime.now())
        SearchPhrase(phrase=phrase).save()

        search_phrase = SearchPhrase.objects.get(phrase=phrase)

        tweets = get_tweets(search_term, username, date, phrase, search_phrase)
        Tweet.objects.bulk_create(tweets)

        tweets = Tweet.objects.filter(search_phrase=search_phrase)

    return render(request, 'api/index.html', {'tweets': tweets, 'message': message})


def search_history(request):
    searches = SearchPhrase.objects.all().order_by()
    return render(request, 'api/search-history.html', {'searches': searches})


def previous_search_results(request, pk):
    return render(request, 'api/previous-search-results.html')


# fetches tweets
def get_tweets(search_term, username, date, phrase, search_phrase):
    base_url = 'https://api.twitter.com/'
    API_KEY='3EKHHmkx3AsMZRKbO0yFtEMJZ'
    API_SECRET='ZQC50IwRoKmjHTytNsVn7lzc2sMj6FW55NoT92xeSlheRxsSAR'
    ACCESS_TOKEN='929630844892753920-e7JREB9wfPtKh4LCmb1QRelbxb4bwXk'
    ACCESS_TOKEN_SECRET='Q8j3s1CcaTq1YRVYHJzE1oag4pSDiO8o7S4EjfrTItNeN'

    auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    search_keyword = ''

    if search_term:
        search_keyword = search_term
    else:
        search_keyword = 'from:'+str(username)

    search_params = {
        'q': search_keyword,
        'result_type': 'recent',
        'until': date,
        'count': 100
    }

    search_url = '{}1.1/search/tweets.json'.format(base_url)
    tweets = requests.get(search_url, params=search_params, auth=auth)
    list_ = []
    # count = 0
    for i in tweets.json()['statuses']:
        s = i['created_at']
        f1 = '%a %b %d %H:%M:%S +0000 %Y'
        f2 = '%Y-%m-%d'
        out = datetime.strptime('Thu Apr 23 13:38:19 +0000 2009', f1).strftime(f2)
        list_.append(Tweet(search_phrase=search_phrase, date=out, user=i['user']['name'], post=i['text'].encode("utf-8")))
    return list_