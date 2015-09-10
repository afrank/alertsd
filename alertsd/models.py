from django.db import models

# this is the top level auth model
class User(models.Model):
    api_key = models.CharField(max_length=64)

# the structure of an alert as it traverses the system
class Alert(models.Model):
    user = models.ForeignKey(User)

# define escalation endpoints: email, HTTP, script
class Escalation(models.Model):
    alert = models.ForeignKey(Alert)

# this is a set of alert criteria you'd use to decide which 
# ruleset to implement for an alert
class Router(models.Model):
    alert = models.ForeignKey(Alert)

# a collection of rules to execute for a given alert. The
# execution of a ruleset guides the alert to either resolution
# or escalation.
class Ruleset(models.Model):
    alert = models.ForeignKey(Alert)

# dictates what to do with an alert once it's received.
class Rules(models.Model):
    ruleset = models.ForeignKey(Ruleset)
    failure_time = models.IntegerField() # the amount of time (in seconds) from when the first alert is received to wait for a recovery before escalating
    max_failures = models.IntegerField() # don't escalate until X failures are received for an alert
    # something about flap detection/mitigation

