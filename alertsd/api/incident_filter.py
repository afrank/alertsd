# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#from django.shortcuts import render_to_response
from alertsd.models import *
from restless.views import Endpoint

from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer

from restless.exceptions import BadRequest

class IncidentFilterResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'alert_id': 'alert_id',
        'regex': 'regex',
        'created_on': 'created_on',
        'updated_on': 'updated_on'
    })
    def list(self):
        return IncidentFilter.objects.filter(alert__user_id=self.user.id)

    def detail(self, pk):
        return IncidentFilter.objects.get(id=pk, alert__user_id=self.user.id)

    def is_authenticated(self):
        if "HTTP_AUTH_TOKEN" in self.request.META:
            auth_token = self.request.META["HTTP_AUTH_TOKEN"]
        else:
            return False
        try:
            self.user = User.objects.get(api_key=auth_token)
        except User.DoesNotExist:
            return False
        return True

    def create(self):
        try:
            alert = Alert.objects.get(pk=self.data['alert_id'], user_id=self.user.id)
        except Alert.DoesNotExist:
            raise BadRequest("Alert Not Found")
        return IncidentFilter.objects.create(alert_id=alert.id, regex=self.data['regex'])

    def update(self, pk):
        try:
            _filter = IncidentFilter.objects.get(id=pk, alert__user_id=self.user.id)
        except IncidentFilter.DoesNotExist:
            raise BadRequest("IncidentFilter Not Found")

        if 'alert_id' in self.data:
            try:
                alert = Alert.objects.get(pk=self.data['alert_id'], user_id=self.user.id)
            except Alert.DoesNotExist:
                raise BadRequest("Alert Not Found")
            _filter.alert_id = alert.id
        if 'regex' in self.data:
            _filter.regex = self.data['regex']
        _filter.save()
        return _filter

    def delete(self, pk):
        try:
            _filter = IncidentFilter.objects.get(id=pk, alert__user_id=self.user.id)
        except IncidentFilter.DoesNotExist:
            raise BadRequest("IncidentFilter not found.")
        _filter.delete()

