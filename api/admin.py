# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from api.models import SearchPhrase, Tweet


admin.site.register(SearchPhrase)
admin.site.register(Tweet)