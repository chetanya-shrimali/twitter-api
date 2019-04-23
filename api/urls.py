from django.conf.urls import url
from api import views

app_name='api'

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^search-history/$', views.index, name='home'),
    url(r'^search-history/(?P<pk>[0-9]+)/$', views.index, name='home'),
]

