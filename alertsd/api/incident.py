# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#from django.shortcuts import render_to_response
from alertsd.models import *
from restless.views import Endpoint

from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer

from restless.exceptions import BadRequest

class IncidentResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'alert_id': 'alert_id',
        'failure_count': 'failure_count',
        'created_on': 'created_on',
        'updated_on': 'updated_on'
    })
    def list(self):
        return Incident.objects.filter(alert__user_id=self.user.id)

    def detail(self, pk):
        return Incident.objects.get(id=pk, alert__user_id=self.user.id)

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
            alert = Alert.objects.get(alert_id=self.data['alert_id'], alert__user_id=self.user.id)
        except Alert.DoesNotExist:
            raise BadRequest("Alert Not Found")
        return Incident.objects.create(alert_id=alert.id)

    def update(self, pk):
        try:
            incident = Incident.objects.get(id=pk, alert__user_id=self.user.id)
        except Incident.DoesNotExist:
            raise BadRequest("Incident Not Found")

        if 'alert_id' in self.data:
            try:
                alert = Alert.objects.get(id=self.data['alert_id'], user_id=self.user.id)
            except Alert.DoesNotExist:
                raise BadRequest("Alert Not Found")
            incident.alert_id = alert.id
        if 'failure_count' in self.data:
            incident.failure_count = self.data['failure_count']
        incident.save()
        return incident

    def delete(self, pk):
        try:
            incident = Incident.objects.get(id=pk, alert__user_id=self.user.id)
        except Incident.DoesNotExist:
            raise BadRequest("Incident not found.")
        incident.delete()

