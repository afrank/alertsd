# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from alertsd.models import *
from restless.views import Endpoint

from restless.exceptions import BadRequest

from alertsd.alert_thread import start_incident_thread

# 
# Alert Handler. This interfaces with the 
# celery code. A request requires 3 things:
# - api_key
# - alert_key
# - action: problem|recovery
#
class AlertEndpoint(Endpoint):
    def post(self,request):
        if "HTTP_AUTH_TOKEN" in self.request.META:
            auth_token = self.request.META["HTTP_AUTH_TOKEN"]
        else:
            raise BadRequest("Auth Token Required")
        if "key" in request.data:
            alert_key = request.data.get('key')
        else:
            raise BadRequest("Alert Key Required")
        if "action" in request.data:
            action = request.data.get('action')
        else:
            raise BadRequest("Action Required")
        try:
            alert = Alert.objects.get(alert_key=alert_key)
        except Alert.DoesNotExist:
            raise BadRequest("Specified Alert Does Not Exist.")

        # check for an existing escalation.
        incident = list(Incident.objects.filter(alert_id=alert.id))
        if len(incident) > 0:
            if action == "resolve":
                # NO LOGS!!!!
                incident[0].delete()
            elif action == "trigger":
                incident[0].failure_count += 1
                incident[0].save()
        else:
            # no previously-reported incident, let's trigger one
            incident = Incident.objects.create(alert_id=alert.id, failure_count=1)
            start_incident_thread.delay(incident.id)
            
        return []

