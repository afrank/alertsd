# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url, include

#from django.contrib import admin
#admin.autodiscover()

from alertsd.default import *
from alertsd.a.user import *
from alertsd.a.escalation import *
from alertsd.a.alert import *

from alertsd.alert.endpoint import *

urlpatterns = patterns('',
    url(r'^$', Healthcheck.as_view(), name='Default'),

    url(r'^a/user/$', UserResource.as_list(), name='api_user_list'),
    url(r'^a/user/(?P<pk>\d+)/$', UserResource.as_detail(), name='api_user_detail'),

    url(r'^a/escalation/$', EscalationResource.as_list(), name='api_escalation_list'),
    url(r'^a/escalation/(?P<pk>\d+)/$', EscalationResource.as_detail(), name='api_escalation_detail'),

    url(r'^a/alert/$', AlertResource.as_list(), name='api_alert_list'),
    url(r'^a/alert/(?P<pk>\d+)/$', AlertResource.as_detail(), name='api_alert_detail'),

    url(r'^alert/$', AlertEndpoint.as_view(), name='AlertEndpoint'),
)
