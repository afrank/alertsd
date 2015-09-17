# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from alertsd.models import *
from restless.views import Endpoint

from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer

from restless.exceptions import BadRequest

class PluginParameterResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'user_id': 'user_id',
        'plugin_id': 'plugin_id',
        'key': 'key',
        'value': 'value',
    })
    def list(self):
        return PluginParameter.objects.filter(user_id=self.user.id)

    def detail(self, pk):
        return PluginParameter.objects.get(id=pk, user_id=self.user.id)

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
        return PluginParameter.objects.create(
            user_id=self.user.id,
            key=self.data['key'],
            value=self.data['value'],
            plugin_id=self.data['plugin_id']
        )

    def update(self, pk):
        try:
            parameter = PluginParameter.objects.get(id=pk, user_id=self.user.id)
        except PluginParameter.DoesNotExist:
            raise BadRequest("PluginParameter not found.")

        if 'plugin_id' in self.data:
            parameter.plugin_id = self.data['plugin_id']
        if 'key' in self.data:
            parameter.key = self.data['key']
        if 'value' in self.data:
            parameter.value = self.data['value']
        parameter.save()
        return parameter

    def delete(self, pk):
        try:
            parameter = PluginParameter.objects.get(id=pk, user_id=self.user.id)
        except PluginParameter.DoesNotExist:
            raise BadRequest("PluginParameter not found.")
        parameter.delete()

