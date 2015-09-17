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
        'failure_expiration': 'failure_expiration',
        'max_failures': 'max_failures',
        'created_on': 'created_on'
    })
    def list(self):
        return Alert.objects.filter(escalation__user_id=self.user.id)

    def detail(self, pk):
        return Alert.objects.get(id=pk, escalation__user_id=self.user.id)

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
            escalation = Escalation.objects.get(id=self.data['escalation_id'], user_id=self.user.id)
        except Escalation.DoesNotExist:
            raise BadRequest("Escalation Does Not Exist")
        return Alert.objects.create(
            alert_key=self.data['alert_key'],
            escalation_id=escalation.id,
            failure_time=self.data['failure_time'],
            failure_expiration=self.data['failure_expiration'],
            max_failures=self.data['max_failures']
        )

    def update(self, pk):
        try:
            alert = Alert.objects.get(id=pk, escalation__user_id=self.user.id)
        except Alert.DoesNotExist:
            raise BadRequest("Alert Not Found")

        if 'alert_key' in self.data:
            alert.alert_key = self.data['alert_key']
        if 'escalation_id' in self.data:
            try:
                escalation = Escalation.objects.get(self.data['escalation_id'], user_id=self.user.id)
            except Escalation.DoesNotExist:
                raise BadRequest("Escalation Does Not Exist")
            alert.escalation_id = escalation.id
        if 'failure_time' in self.data:
            alert.failure_time = self.data['failure_time']
        if 'max_failures' in self.data:
            alert.max_failures = self.data['max_failures']
        if 'failure_expiration' in self.data:
            alert.failure_expiration = self.data['failure_expiration']
        alert.save()
        return alert

    def delete(self, pk):
        try:
            alert = Alert.objects.get(id=pk, escalation__user_id=self.user.id)
        except Alert.DoesNotExist:
            raise BadRequest("Alert not found.")
        alert.delete()

