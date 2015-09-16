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
        return Incident.objects.all()

    def detail(self, pk):
        return Incident.objects.get(id=pk)

    def is_authenticated(self):
        return True

    def create(self):
        return Incident.objects.create(alert_id=self.data['alert_id'])

    def update(self, pk):
        try:
            incident = Incident.objects.get(id=pk)
        except Incident.DoesNotExist:
            incident = Incident()

        if 'alert_id' in self.data:
            incident.alert_id = self.data['alert_id']
        if 'failure_count' in self.data:
            incident.failure_count = self.data['failure_count']
        incident.save()
        return incident

    def delete(self, pk):
        try:
            incident = Incident.objects.get(id=pk)
        except Incident.DoesNotExist:
            raise BadRequest("Incident not found.")
        incident.delete()

