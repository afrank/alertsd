from django.db import models

# this is the top level auth model
class User(models.Model):
    api_key = models.CharField(max_length=64)

#class AlertRuleset(models.Model):
#    user = models.ForeignKey(User)
#    match_style = models.CharField(max_length=10) # ALL, ANY

# a collection of rules to execute for a given alert. The
# execution of a ruleset guides the alert to either resolution
# or escalation.
class EscalationRuleset(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=16)

# the structure of an alert as it traverses the system.
class Alert(models.Model):
    match_key = models.CharField(max_length=255) # this is the key used to call this alert in the API
    escalation_ruleset = models.ForeignKey(EscalationRuleset)
    escalation_target = models.ForeignKey(EscalationTarget)
    created_on = models.DateTimeField(auto_now_add=True,auto_now=False)
    #alert_match_style = models.CharField(max_length=10) # ANY, ALL -- this relates to how associated AlertRules are applied
    failure_time = models.IntegerField() # the amount of time (in seconds) from when the first alert is received to wait for a recovery before escalating
    max_failures = models.IntegerField() # don't escalate until X failures are received for an alert
    # TODO something about flap detection/mitigation
    # TODO escalation persistence

# this is a set of alert criteria you'd use to decide which 
# ruleset to implement for an alert.
# It's basically regex rules that apply to either the headers or the body
# of the alert.
#class AlertRules(models.Model):
#    alert = models.ForeignKey(Alert)
#    pattern_type = models.CharField(max_length=64) # header, message
#    pattern = models.CharField(max_length=255)

class EscalationTarget(models.Model):
    user = models.ForeignKey(User)
    escalation_type = models.CharField(max_length=10) # email, HTTP, script
    escalate_every = models.IntegerField(default=0) # setting this to >0 will result in a recurring escalation

# dictates what to do with an alert once it's received.
#class EscalationRules(models.Model):
#    escalation_ruleset = models.ForeignKey(EscalationRuleset)
#    failure_time = models.IntegerField() # the amount of time (in seconds) from when the first alert is received to wait for a recovery before escalating
#    max_failures = models.IntegerField() # don't escalate until X failures are received for an alert
#    # TODO something about flap detection/mitigation

