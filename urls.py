# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url, include

from django.contrib import admin
admin.autodiscover()

from alertsd.api.default import *

urlpatterns = patterns('',
    url(r'^$', Healthcheck.as_view(), name='Default'),
)
