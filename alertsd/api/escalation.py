# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from alertsd.models import *
from restless.views import Endpoint

from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer

from restless.exceptions import BadRequest

class EscalationResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'user_id': 'user_id',
        'escalation_interval': 'escalation_interval',
        'plugin': 'plugin',
    })
    def list(self):
        return Escalation.objects.filter(user_id=self.user.id)

    def detail(self, pk):
        return Escalation.objects.get(id=pk, user_id=self.user.id)

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
        return Escalation.objects.create(
            user_id=self.user.id,
            escalation_interval=self.data['escalation_interval'],
            plugin=self.data['plugin']
        )

    def update(self, pk):
        try:
            escalation = Escalation.objects.get(id=pk, user_id=self.user.id)
        except Escalation.DoesNotExist:
            raise BadRequest("Escalation not found.")

        if 'user_id' in self.data:
            escalation.api_key = self.data['user_id']
        if 'escalation_interval' in self.data:
            escalation.escalation_interval = self.data['escalation_interval']
        if 'plugin' in self.data:
            escalation.plugin = self.data['plugin']
        escalation.save()
        return escalation

    def delete(self, pk):
        try:
            escalation = Escalation.objects.get(id=pk, user_id=self.user.id)
        except Escalation.DoesNotExist:
            raise BadRequest("Escalation not found.")
        escalation.delete()

