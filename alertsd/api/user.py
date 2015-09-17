# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#from django.shortcuts import render_to_response
from alertsd.models import *
from restless.views import Endpoint

from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer

from restless.exceptions import BadRequest

class UserResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'api_key': 'api_key',
    })
    def list(self):
        return User.objects.all()

    def detail(self, pk):
        return User.objects.get(id=pk)

    def is_authenticated(self):
        whitelisted_ips = ['127.0.0.1']
        if self.request.META.get('REMOTE_ADDR') not in whitelisted_ips:
            return False
        return True

    def create(self):
        return User.objects.create(
            api_key=self.data['api_key']
        )

    def update(self, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            user = User()

        if 'api_key' in self.data:
            user.api_key = self.data['api_key']
        user.save()
        return user

    def delete(self, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            raise BadRequest("User not found.")
        user.delete()

