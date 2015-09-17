# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from alertsd.models import *
from restless.views import Endpoint

from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer

from restless.exceptions import BadRequest

class PluginResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'name': 'name',
        'path': 'path',
        'required_parameters': 'required_parameters',
        'created_on': 'created_on',
        'updated_on': 'updated_on'
    })
    def list(self):
        return Plugin.objects.all()

    def detail(self, pk):
        return Plugin.objects.get(id=pk)

    def is_authenticated(self):
        self.writable = False
        whitelisted_ips = ['127.0.0.1']
        if self.request.META.get('REMOTE_ADDR') in whitelisted_ips or self.request.META.get('HTTP_X_REAL_IP') in whitelisted_ips:
            self.writable = True
            return True
        else:
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
        if self.writable is True:
            return Plugin.objects.create(
                name=self.data['name'],
                path=self.data['path'],
                required_parameters=self.data['required_parameters']
            )
        else:
            raise BadRequest("Writable Access not possible")

    def update(self, pk):
        if self.writable is True:
            try:
                plugin = Plugin.objects.get(id=pk)
            except Plugin.DoesNotExist:
                raise BadRequest("Plugin Not Found")

            if 'name' in self.data:
                plugin.name = self.data['name']
            if 'path' in self.data:
                plugin.path = self.data['path']
            if 'required_parameters' in self.data:
                plugin.required_parameters = self.data['required_parameters']
            plugin.save()
            return plugin
        else:
            raise BadRequest("Writable Access not possible")

    def delete(self, pk):
        if self.writable is True:
            try:
                plugin = Plugin.objects.get(id=pk)
            except Plugin.DoesNotExist:
                raise BadRequest("Plugin not found.")
            plugin.delete()
        else:
            raise BadRequest("Writable Access not possible")

