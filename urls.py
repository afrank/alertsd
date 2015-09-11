# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url, include

from django.contrib import admin
admin.autodiscover()

from alertsd.api.default import *
from alertsd.api.user import *

urlpatterns = patterns('',
    url(r'^$', Healthcheck.as_view(), name='Default'),
    url(r'^api/user/$', UserResource.as_list(), name='api_user_list'),
    url(r'^api/user/(?P<pk>\d+)/$', UserResource.as_detail(), name='api_user_detail'),
)
