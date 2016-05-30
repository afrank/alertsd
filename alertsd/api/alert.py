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
        'plugin': 'plugin.name',
        'key': 'key',
        'failure_time': 'failure_time',
        'failure_expiration': 'failure_expiration',
        'max_failures': 'max_failures',
        'created_on': 'created_on'
    })
    def list(self):
        return Alert.objects.filter(user_id=self.user.id)

    def detail(self, name):
        return Alert.objects.get(key=name, user_id=self.user.id)

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
            plugin = Plugin.objects.get(id=self.data['plugin_id'])
        except Plugin.DoesNotExist:
            raise BadRequest("Plugin Does Not Exist")
        return Alert.objects.create(
            key=self.data['key'],
            plugin_id=plugin.id,
            user_id=self.user.id,
            failure_time=self.data['failure_time'],
            failure_expiration=self.data['failure_expiration'],
            max_failures=self.data['max_failures']
        )

    def update(self, pk):
        try:
            alert = Alert.objects.get(id=pk, user_id=self.user.id)
        except Alert.DoesNotExist:
            raise BadRequest("Alert Not Found")

        if 'key' in self.data:
            alert.key = self.data['key']
        if 'plugin_id' in self.data:
            try:
                plugin = Plugin.objects.get(pk=self.data['plugin_id'])
            except Plugin.DoesNotExist:
                raise BadRequest("Plugin Does Not Exist")
            alert.plugin_id = plugin.id
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
            alert = Alert.objects.get(id=pk, user_id=self.user.id)
        except Alert.DoesNotExist:
            raise BadRequest("Alert not found.")
        alert.delete()

