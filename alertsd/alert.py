# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from alertsd.models import *
from restless.views import Endpoint

from restless.exceptions import BadRequest

from alertsd.async import start_incident_thread

# 
# Alert Handler. This interfaces with the 
# celery code. A request requires 3 things:
# - api_key
# - alert_key
# - action: trigger|resolve
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
        if "comment" in request.data:
            comment = request.data.get('comment')
        else:
            comment = ""
        try:
            user = User.objects.get(api_key=auth_token)
        except User.DoesNotExist:
            raise BadRequest("User Does Not Exist")

        try:
            alert = Alert.objects.get(alert_key=alert_key,escalation__user_id=user.id)
        except Alert.DoesNotExist:
            raise BadRequest("Specified Alert Does Not Exist.")

        # see if there are any filters that would prevent this from triggering
        if comment <> "":
            filters = list(AlertFilter.objects.filter(alert_id=alert.id))
            if len(filters) > 0:
                import re
                for f in filters:
                    if re.match(f.regex,comment) is not None:
                        return {'msg':'Not Triggering since comment string matches associated filter %s' % str(f.id)}

        # check for an existing escalation.
        try:
            incident = Incident.objects.get(alert_id=alert.id)
            if action == "resolve":
                # NO LOGS!!!!
                incident.delete()
                return []
            elif action == "trigger":
                incident.failure_count += 1
                incident.save()
        except Incident.DoesNotExist:
            incident = Incident.objects.create(alert_id=alert.id, failure_count=1)
            start_incident_thread.delay(incident.id)

        return {"alert_id":incident.alert_id, "failure_count":incident.failure_count, "created_on":incident.created_on, "updated_on":incident.updated_on}

