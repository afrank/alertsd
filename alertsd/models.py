from django.db import models

# this is the top level auth model
class User(models.Model):
    api_key = models.CharField(max_length=64, unique=True)

class Escalation(models.Model):
    user = models.ForeignKey(User)
    escalation_type = models.CharField(max_length=10) # email, HTTP, script, stdout
    escalation_interval = models.IntegerField(default=0) # setting this to >0 will result in a recurring escalation
    endpoint = models.CharField(max_length=255) # this will be an email address, a script, or a url. TODO: HTTP type support will require a lot more stuff to be awesome.

# the structure of an alert as it traverses the system.
class Alert(models.Model):
    alert_key = models.CharField(max_length=255, unique=True) # this is the key used to call this alert in the API
    escalation = models.ForeignKey(Escalation)
    created_on = models.DateTimeField(auto_now_add=True,auto_now=False)
    failure_time = models.IntegerField() # the amount of time (in seconds) from when the first alert is received to wait for a recovery before escalating
    max_failures = models.IntegerField() # don't escalate until X failures are received for an alert
    # TODO something about flap detection/mitigation
    # TODO escalation persistence

# this is basically a cache where active escalations will be tracked.
class Incident(models.Model):
    alert = models.ForeignKey(Alert, unique=True) # unique -- can only have one active instnace of an alert at a time
    failure_count = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_on = models.DateTimeField(auto_now_add=True,auto_now=True)
