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
            plugin = Plugin.objects.get(pk=alert.plugin_id)
            plugin_parameters = list(PluginParameter.objects.filter(plugin_id=plugin.id))
            print "Escalating incident_id %s alert_id %s using %s plugin" % (str(incident_id), str(alert.id), plugin.name)
            import subprocess
            import os


            plugin_path = "plugins/%s" % plugin.path
            if not os.path.isfile(plugin_path):
                print "Cannot escalate because plugin does not exist: %s" % plugin_path
                incident.delete()
                break

            sub_env = os.environ.copy()
            sub_env["ALERT_KEY"] = str(alert.key)
            sub_env["FAILURE_COUNT"] = str(incident.failure_count)
            sub_env["INCIDENT_START"] = str(start_time)
            sub_env["INCIDENT_DETAILS"] = str(incident.value)
            if len(plugin_parameters) > 0:
                for parameter in plugin_parameters:
                    sub_env[parameter.key] = str(parameter.value)
            if ',' in plugin.required_parameters:
                required_parameters = plugin.required_parameters.split(',')
            elif plugin.required_parameters <> "":
                required_parameters = [plugin.required_parameters]
            else:
                required_parameters = []
            missing_params = []
            for p in required_parameters:
                if p.strip() not in sub_env:
                    missing_params += [p.strip()]
            if len(missing_params) > 0:
                print "Cannot escalate because required parameters are missing: ", missing_params
                incident.delete()
                break
            print "Starting subprocess for %s" % plugin_path
            print(subprocess.Popen(plugin_path, env=sub_env))
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
