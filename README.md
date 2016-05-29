# alertsd

Doing alerts right is kinda hard. In the glorious world of devops, you want to do adhoc alerting, where you've got a few different products all implementing their own alerting rules, tied in to any number of things. Finding something wrong and sending an alert is not too tough, but implementing certain alerting concepts like escalations, flap detection, check intervals, notification intervals, etc. are non-trivial, and take away from more important tasks (like improving your application!). Ok, so why not just use nagios, or something like it. Well, you can! But setting up nagios is non-trivial and could be a bit heavy-handed depending on your use case.

To clearly see how alertsd fits into a monitoring workflow, let's consider monitoring as comprised of three distinct concepts: Monitoring, Alerting and Notification. The distinction between Monitoring/Alerting and Notification is widely-established; as apps have moved into public clouds where doing email-based notifications isn't as easy as it used to be (or maybe you just don't want to run your own SMTP), notifications are increasingly handled by 3rd-party services (Pagerduty is excellent at this). Alertsd goes one step further and breaks up the relationship between monitoring and alerting.

Example Workflow:

- Monitoring: A monitor can be as simple as a curl against a web port, or a cron job that scrapes a log. It doesn't need to maintain state, because that happens at the Alert layer. (TODO: Provide example monitors)
- Alerting: When a monitor discovers a problem, it makes an API call to the alerting layer (alertsd), which maintains the state of the alert, and knows certain things, like how many failures can happen in a given time box before escalating to the Notification layer.
- If an alert has received a sufficient number of failures from a monitor it will trigger a notification. It uses an escalation plugin to interface with an external notification layer, like SMTP, or preferrably Pagerduty.

Another benefit of something like this is it gives you an escalation proxy, so instead of having a bunch of nodes sending email or making API calls to pagerduty, you can do all that from here. *Your firewall will thank you*.

## Installing
Alertsd is dockerized, so you can install the latest version simply by running `docker pull afrank/alertsd` then `docker run -p 8080:8080 -d afrank/alertsd`. If you're undocker, you can also play around with the [install.sh](install.sh) script. Once you've installed the container, you will want to add a user and an alerting target.

### Create a user
```
api_key=$(uuidgen)
base_url=http://localhost:8080
curl -s -X POST -d "{\"api_key\":\"$api_key\"}" $base_url/api/user/ | python -m json.tool
```

### List available plugins
```
curl -s -X GET -H "Auth-Token: $api_key" $base_url/api/plugin/ | python -m json.tool
```

### Create an alerting target
```
plugin_id=3
curl -s -X POST -H "Auth-Token: $api_key" -d '{"key":"testing.key","plugin_id":$plugin_id,"failure_time":300,"max_failures":5,"failure_expiration":60}' $base_url/api/alert/ | python -m json.tool
# record your alert_id
```
If you're using a plugin that requires parameters (like pagerduty), you should associate those parameters with your alert/plugin pair:
```
alert_id=1
curl -s -X POST -H "Auth-Token: $api_key" -d '{"plugin_id":$plugin_id,"alert_id":$alert_id,"key":"api_key","value":"YOUR_PAGERDUTY_API_KEY"}' $base_url/api/plugin/parameter/ | python -m json.tool
curl -s -X POST -H "Auth-Token: $api_key" -d '{"plugin_id":$plugin_id,"alert_id":$alert_id,"key":"service_key","value":"YOUR_PAGERDUTY_SERVICE_KEY"}' $base_url/api/plugin/parameter/ | python -m json.tool
```

## A note about plugins
Plugins dictate the way escalations are handled. When an incident is escalated based on the alert rules, the plugin is executed as a sub-process with various things passed to it as environment variables. Using the sub-process with environment variables means plugins can be written in any scripting language.

## Client Library

A basic python client library is included. It can be installed by running `sudo pip install --upgrade git+https://github.com/afrank/alertsd`.

Example Usage:
```
#!/usr/bin/python

from alertsd import Alertsd

api_key = "7f8b419a-25bb-11e6-a813-002590eb817c" # this is just a made-up string

c = Alertsd('http://localhost:8080',api_key)

print(c.create_user())

key = 'testing.key'

print(c.create_alert(key, plugin='pagerduty', failure_time=300, max_failures=5, failure_expiration=60))
print(c.add_param(key,'pagerduty','api_key','YOUR_PAGERDUTY_API_KEY'))
print(c.add_param(key,'pagerduty','service_key','YOUR_PAGERDUTY_SERVICE_KEY'))

print(c.trigger(key,'OMG EVERYTHING IS ON FIRE!!!!'))
```
