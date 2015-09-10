from django.db import models

# this is the top level auth model
class User(models.Model):
    api_key = models.CharField(max_length=64)

class AlertRuleset(models.Model):
    user = models.ForeignKey(User)

# the structure of an alert as it traverses the system.
class Alert(models.Model):
    alert_ruleset = models.ForeignKey(AlertRuleset)

# define escalation endpoints: email, HTTP, script
class Escalation(models.Model):
    alert = models.ForeignKey(Alert)
    # TODO escalation persistence

# this is a set of alert criteria you'd use to decide which 
# ruleset to implement for an alert.
# It's basically regex rules that apply to either the headers or the body
# of the alert.
class AlertRules(models.Model):
    alert_ruleset = models.ForeignKey(AlertRuleset)
    pattern_type = models.CharField(max_length=64) # header, message
    pattern = models.CharField(max_length=255)

# a collection of rules to execute for a given alert. The
# execution of a ruleset guides the alert to either resolution
# or escalation.
class EscalationRuleset(models.Model):
    alert = models.ForeignKey(Alert)

# dictates what to do with an alert once it's received.
class EscalationRules(models.Model):
    ruleset = models.ForeignKey(Ruleset)
    failure_time = models.IntegerField() # the amount of time (in seconds) from when the first alert is received to wait for a recovery before escalating
    max_failures = models.IntegerField() # don't escalate until X failures are received for an alert
    # TODO something about flap detection/mitigation

