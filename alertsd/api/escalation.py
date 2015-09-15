# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#from django.shortcuts import render_to_response
from alertsd.models import *
from restless.views import Endpoint

from restless.dj import DjangoResource
from restless.preparers import FieldsPreparer

from restless.exceptions import BadRequest

class EscalationResource(DjangoResource):
    preparer = FieldsPreparer(fields={
        'id': 'id',
        'user_id': 'user_id',
        'escalation_type': 'escalation_type',
        'escalation_interval': 'escalation_interval',
    })
    def list(self):
        return Escalation.objects.all()

    def detail(self, pk):
        return Escalation.objects.get(id=pk)

    def is_authenticated(self):
        return True

    def create(self):
        return Escalation.objects.create(
            user_id=self.data['user_id'],
            escalation_type=self.data['escalation_type'],
            escalation_interval=self.data['escalation_interval']
        )

    def update(self, pk):
        try:
            escalation = Escalation.objects.get(id=pk)
        except Escalation.DoesNotExist:
            escalation = Escalation()

        if 'user_id' in self.data:
            escalation.api_key = self.data['user_id']
        if 'escalation_type' in self.data:
            escalation.escalation_type = self.data['escalation_type']
        if 'escalation_interval' in self.data:
            escalation.escalation_interval = self.data['escalation_interval']
        escalation.save()
        return escalation

    def delete(self, pk):
        try:
            escalation = Escalation.objects.get(id=pk)
        except Escalation.DoesNotExist:
            raise BadRequest("Escalation not found.")
        escalation.delete()

