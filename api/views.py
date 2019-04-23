# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
from requests_oauthlib import OAuth1

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from api.models import SearchPhrase, Tweet
from datetime import datetime
from credentials import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


def index(request):
    # sending request
    search_term = request.GET.get('search_term')
    username = request.GET.get('username')
    date = request.GET.get('date')
    page = request.GET.get('page')

    tweets = ''
    message = ''

    if not search_term and not username and not page:
        message = 'Please enter the values to fetch tweet results!'
    else:
        phrase = str(search_term) + ' ' + str(username) + ' ' + str(date) + ' ' + str(datetime.now())
        SearchPhrase(phrase=phrase).save()

        search_phrase = SearchPhrase.objects.get(phrase=phrase)

        tweets = get_tweets(search_term, username, date, phrase, search_phrase)
        Tweet.objects.bulk_create(tweets)

        tweets_list = Tweet.objects.filter(search_phrase=search_phrase)
        paginator = Paginator(tweets_list, 10)
        try:
            tweets = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            tweets = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            tweets = paginator.page(paginator.num_pages)
    return render(request, 'api/index.html', {'tweets': tweets, 'message': message})


def search_history(request):
    searches = SearchPhrase.objects.all().order_by('-date')
    return render(request, 'api/search-history.html', {'searches': searches})


def previous_search_results(request, pk):
    tweets = Tweet.objects.filter(search_phrase=SearchPhrase.objects.get(pk=pk))
    return render(request, 'api/previous-search-results.html', {'tweets':tweets})


# fetches tweets
def get_tweets(search_term, username, date, phrase, search_phrase):
    base_url = 'https://api.twitter.com/'

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