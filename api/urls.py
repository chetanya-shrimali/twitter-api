from django.conf.urls import url
from api import views

app_name='api'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search-history/$', views.search_history, name='search-history'),
    url(r'^search-history/(?P<pk>[0-9]+)/$', views.previous_search_results, name='previous-results'),
]

