# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import requests
from requests_oauthlib import OAuth1

def index(request):
    # sending request
    search_term = request.GET.get('search_term')
    username = request.GET.get('username')
    date = request.GET.get('date')
    tweets = get_tweets(search_term, username, date)

    # print(tweets[0])
    return render(request, 'api/index.html', {'tweets': tweets})


# fetches tweets
def get_tweets(search_term, username, date):
    base_url = 'https://api.twitter.com/'
    API_KEY='3EKHHmkx3AsMZRKbO0yFtEMJZ'
    API_SECRET='ZQC50IwRoKmjHTytNsVn7lzc2sMj6FW55NoT92xeSlheRxsSAR'
    ACCESS_TOKEN='929630844892753920-e7JREB9wfPtKh4LCmb1QRelbxb4bwXk'
    ACCESS_TOKEN_SECRET='Q8j3s1CcaTq1YRVYHJzE1oag4pSDiO8o7S4EjfrTItNeN'

    auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


    search_params = {
        'q': search_term,
        'result_type': 'recent',
        'until': date,
        'count': 100
    }

    search_url = '{}1.1/search/tweets.json'.format(base_url)
    tweets = requests.get(search_url, params=search_params, auth=auth)
    list_ = []
    count = 0
    for i in tweets.json()['statuses']:
        count += 1
        list_.append([count, i['created_at'], i['user']['name'], i['text']])
    return list_