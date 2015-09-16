from __future__ import absolute_import

from alertsd.models import *

from celery import shared_task

import time

@shared_task
def start_incident_thread(incident_id):
    start_time = time.time()
    while True:
        now = time.time()
        try:
            incident = Incident.objects.get(pk=incident_id)
        except Incident.DoesNotExist:
            # the incident has already been resolved, so just break out
            break
        alert = Alert.objects.get(pk=incident.alert_id)
        if (alert.failure_time > 0 and now-start_time > alert.failure_time) or (alert.max_failures > 0 and incident.failure_count >= alert.max_failures):
            # ESCALATE!
            escalation = Escalation.objects.get(pk=alert.escalation_id)
            if escalation.escalation_type == "stdout":
                print "STDOUT Escalation for %s" % str(alert.alert_key)
            incident.delete()
            break
        else:
            time.sleep(5)
