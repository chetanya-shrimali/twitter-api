from django.conf.urls import url
from api import views

app_name='api'

urlpatterns = [
    url(r'^$', views.index, name='home')
]

