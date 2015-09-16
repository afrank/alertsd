# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url, include

#from django.contrib import admin
#admin.autodiscover()

from alertsd.default import *
from alertsd.api.user import UserResource
from alertsd.api.escalation import EscalationResource
from alertsd.api.alert import AlertResource
from alertsd.api.incident import IncidentResource

from alertsd.alert import AlertEndpoint

urlpatterns = patterns('',
    url(r'^$', Healthcheck.as_view(), name='Default'),

    url(r'^api/user/$', UserResource.as_list(), name='api_user_list'),
    url(r'^api/user/(?P<pk>\d+)/$', UserResource.as_detail(), name='api_user_detail'),

    url(r'^api/escalation/$', EscalationResource.as_list(), name='api_escalation_list'),
    url(r'^api/escalation/(?P<pk>\d+)/$', EscalationResource.as_detail(), name='api_escalation_detail'),

    url(r'^api/alert/$', AlertResource.as_list(), name='api_alert_list'),
    url(r'^api/alert/(?P<pk>\d+)/$', AlertResource.as_detail(), name='api_alert_detail'),

    url(r'^api/incident/$', IncidentResource.as_list(), name='api_incident_list'),
    url(r'^api/incident/(?P<pk>\d+)/$', IncidentResource.as_detail(), name='api_incident_detail'),

    url(r'^alert/$', AlertEndpoint.as_view(), name='AlertEndpoint'),
)
