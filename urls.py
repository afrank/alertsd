# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url, include

#from django.contrib import admin
#admin.autodiscover()

from alertsd.default import *
from alertsd.api.user import UserResource
from alertsd.api.alert import AlertResource
from alertsd.api.incident import IncidentResource
from alertsd.api.incident_filter import IncidentFilterResource
from alertsd.api.plugin import PluginResource
from alertsd.api.plugin_parameter import PluginParameterResource

from alertsd.alert import AlertEndpoint

urlpatterns = patterns('',
    url(r'^$', Healthcheck.as_view(), name='Default'),

    url(r'^api/user/$', UserResource.as_list(), name='api_user_list'),
    url(r'^api/user/(?P<pk>\d+)/$', UserResource.as_detail(), name='api_user_detail'),

    url(r'^api/alert/$', AlertResource.as_list(), name='api_alert_list'),
    url(r'^api/alert/(?P<name>.+)/$', AlertResource.as_detail(), name='api_alert_detail'),

    url(r'^api/incident/$', IncidentResource.as_list(), name='api_incident_list'),
    url(r'^api/incident/(?P<pk>\d+)/$', IncidentResource.as_detail(), name='api_incident_detail'),

    url(r'^api/incident/filter/$', IncidentFilterResource.as_list(), name='api_incident_filter_list'),
    url(r'^api/incident/filter/(?P<pk>\d+)/$', IncidentFilterResource.as_detail(), name='api_incident_filter_detail'),

    url(r'^api/plugin/$', PluginResource.as_list(), name='api_plugin_list'),
    url(r'^api/plugin/(?P<name>.+)/$', PluginResource.as_detail(), name='api_plugin_detail'),

    url(r'^api/plugin_parameter/$', PluginParameterResource.as_list(), name='api_plugin_parameter_list'),
    url(r'^api/plugin_parameter/(?P<pk>\d+)/$', PluginParameterResource.as_detail(), name='api_plugin_parameter_detail'),

    url(r'^alert/$', AlertEndpoint.as_view(), name='AlertEndpoint'),
)
