from django.db import models

# this is the top level auth model
class User(models.Model):
    api_key = models.CharField(max_length=64, unique=True)
    created_on = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_on = models.DateTimeField(auto_now_add=True,auto_now=True)

# this is a top-level endpoint, readable by anyone with an api_key, writable only by localhost
# these are escalation plugins that get called via subprocesses with parameters passed via environment
# variables.
class Plugin(models.Model):
    name = models.CharField(max_length=25, unique=True)
    path = models.CharField(max_length=255) # this is chrooted to <BASEDIR>/plugins
    required_parameters = models.CharField(max_length=255) # comma-delimited list of variables the plugin depends on
    created_on = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_on = models.DateTimeField(auto_now_add=True,auto_now=True)

# these are simply parameters, like api keys, that are passed to plugins when they're excecuted, as environment variables
class PluginParameter(models.Model):
    user = models.ForeignKey(User)
    plugin = models.ForeignKey(Plugin)
    key = models.CharField(max_length=25)
    value = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_on = models.DateTimeField(auto_now_add=True,auto_now=True)

# the structure of an alert as it traverses the system.
class Alert(models.Model):
    key = models.CharField(max_length=255, unique=True) # this is the key used to call this alert in the API
    plugin = models.ForeignKey(Plugin)
    created_on = models.DateTimeField(auto_now_add=True,auto_now=False)
    failure_time = models.IntegerField(default=0) # the amount of time (in seconds) from when the first alert is received to wait for a recovery before escalating
    max_failures = models.IntegerField(default=0) # don't escalate until X failures are received for an alert
    failure_expiration = models.IntegerField(default=0) # if an alert isn't escalated within X seconds the incident will be resolved
    updated_on = models.DateTimeField(auto_now_add=True,auto_now=True)
    # TODO something about flap detection/mitigation
    # TODO escalation persistence

# this is basically a cache where active escalations will be tracked.
class Incident(models.Model):
    alert = models.ForeignKey(Alert)
    value = models.CharField(max_length=255, default="")
    failure_count = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_on = models.DateTimeField(auto_now_add=True,auto_now=True)

class IncidentFilter(models.Model):
    alert = models.ForeignKey(Alert)
    regex = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_on = models.DateTimeField(auto_now_add=True,auto_now=True)

