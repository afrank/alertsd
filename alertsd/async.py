from __future__ import absolute_import

from alertsd.models import *

from celery import shared_task

import time

@shared_task
def start_incident_thread(incident_id):
    sleep_time = 5
    start_time = time.time()
    last_trigger = 0
    trigger_count = 0
    while True:
        print "Waking up..."
        now = time.time()
        print "This thread has been running for %s seconds." % str(now-start_time)
        try:
            incident = Incident.objects.get(pk=incident_id)
        except Incident.DoesNotExist:
            # the incident has already been resolved, so just break out
            print "No incident exists for incident_id %s, exiting thread." % str(incident_id)
            break
        if incident.failure_count > trigger_count:
            last_trigger = time.time()
            trigger_count = incident.failure_count
            print "Trigger has been incremented, current value: %s" % str(trigger_count)
        alert = Alert.objects.get(pk=incident.alert_id)
        if (alert.failure_time > 0 and now-start_time > alert.failure_time) or (alert.max_failures > 0 and incident.failure_count >= alert.max_failures):
            # ESCALATE!
            print "Escalating incident_id %s alert_id %s" % (str(incident_id), str(alert.id))
            escalation = Escalation.objects.get(pk=alert.escalation_id)
            if escalation.escalation_type == "stdout":
                print "STDOUT Escalation for %s" % str(alert.alert_key)
            incident.delete()
            break
        elif alert.failure_time == 0 and alert.failure_expiration > 0 and last_trigger > 0 and now-last_trigger > alert.failure_expiration:
            # incident has expired
            print "Incident id# %s has expired, exiting thread." % str(incident_id)
            incident.delete()
            break
        else:
            print "Seconds since last trigger: %s" % str(now-last_trigger)
            print "Sleeping for %s seconds." % str(sleep_time)
            incident = None
            time.sleep(sleep_time)
