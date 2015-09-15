# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#from django.shortcuts import render_to_response
from alertsd.models import *
from restless.views import Endpoint

from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer

from restless.exceptions import BadRequest

class AlertResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'escalation_id': 'escalation_id',
        'alert_key': 'alert_key',
        'failure_time': 'failure_time',
        'max_failures': 'max_failures',
        'created_on': 'created_on'
    })
    def list(self):
        return Alert.objects.all()

    def detail(self, pk):
        return Alert.objects.get(id=pk)

    def is_authenticated(self):
        return True

    def create(self):
        return Alert.objects.create(
            alert_key=self.data['alert_key'],
            escalation_id=self.data['escalation_id'],
            failure_time=self.data['failure_time'],
            max_failures=self.data['max_failures']
        )

    def update(self, pk):
        try:
            alert = Alert.objects.get(id=pk)
        except Alert.DoesNotExist:
            alert = Alert()

        if 'alert_key' in self.data:
            alert.alert_key = self.data['alert_key']
        if 'escalation_id' in self.data:
            alert.escalation_id = self.data['escalation_id']
        if 'failure_time' in self.data:
            alert.failure_time = self.data['failure_time']
        if 'max_failures' in self.data:
            alert.max_failures = self.data['max_failures']
        alert.save()
        return alert

    def delete(self, pk):
        try:
            alert = Alert.objects.get(id=pk)
        except Alert.DoesNotExist:
            raise BadRequest("Alert not found.")
        Alert.delete()

