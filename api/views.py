# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
from requests_oauthlib import OAuth1

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from api.models import SearchPhrase, Tweet
from datetime import datetime
from credentials import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


def index(request):
    # Getting request parameters
    search_term = request.GET.get('search_term')
    username = request.GET.get('username')
    date = request.GET.get('date')
    page = request.GET.get('page')

    tweets = ''
    message = ''

    # If we have search term or username in the parameters
    if all(elem in request.GET for elem in ['search_term', 'username']):
        sub_phrase = str(search_term) + ' ' + str(username) + ' ' + str(date)
        phrase = sub_phrase + ' ' + str(datetime.now())
        if not page:


            if not username and not search_term:
                return "Do not enter"

            # Saves search phrase for tracking history History
            SearchPhrase(phrase=phrase).save()

            search_phrase = SearchPhrase.objects.get(phrase=phrase)

            # Get tweets list from the function
            tweets = get_tweets(search_term, username, date, phrase, search_phrase)
            Tweet.objects.bulk_create(tweets)

            tweets_list = Tweet.objects.filter(search_phrase=search_phrase)

            tweets = paginator_handler(tweets_list, page)
        else:
            # for pagination
            latest = SearchPhrase.objects.all().order_by('-date')[0]
            tweets_list = Tweet.objects.filter(search_phrase=latest)

            tweets = paginator_handler(tweets_list, page)
    else:
        message = 'Please enter the search term or username to get the tweets'
    return render(request, 'api/index.html', {'tweets': tweets, 'message': message})


# shows all the search history
def search_history(request):
    searches = SearchPhrase.objects.all().order_by('-date')
    return render(request, 'api/search-history.html', {'searches': searches})


# shows all the previous search results
def previous_search_results(request, pk):
    page = request.GET.get('page')
    tweets_list = Tweet.objects.filter(search_phrase=SearchPhrase.objects.get(pk=pk))
    tweets = paginator_handler(tweets_list, page)
    return render(request, 'api/previous-search-results.html', {'tweets':tweets})


# fetches tweets from twitter
def get_tweets(search_term, username, date, phrase, search_phrase):
    base_url = 'https://api.twitter.com/'

    auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    search_keyword = ''

    if search_term:
        search_keyword = search_term
    else:
        search_keyword = 'from:'+str(username)
    if not date:
        date = datetime.now().strftime ("%Y-%m-%d")
    search_params = {
        'q': search_keyword,
        'result_type': 'recent',
        'until': date,
        'count': 100
    }

    search_url = '{}1.1/search/tweets.json'.format(base_url)
    tweets = requests.get(search_url, params=search_params, auth=auth)
    # creating Tweet model objects to be added to database
    list_ = []
    # count = 0
    for i in tweets.json()['statuses']:
        s = i['created_at']
        f1 = '%a %b %d %H:%M:%S +0000 %Y'
        f2 = '%Y-%m-%d'
        out = datetime.strptime(s, f1).strftime(f2)
        list_.append(Tweet(search_phrase=search_phrase, date=out, user=i['user']['name'], post=i['text'].encode("utf-8")))
    return list_

# Handles the pagination functions
def paginator_handler(tweets_list, page):
    # paginator to paginate the tweets
    paginator = Paginator(tweets_list, 10)

    try:
        tweets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tweets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tweets = paginator.page(paginator.num_pages)

    return tweets