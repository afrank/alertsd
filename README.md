# alertsd

Doing alerts right is kinda hard. In the glorious world of devops, you want to do adhoc alerting, where you've got a few different products all implementing their own alerting rules, tied in to any number of things. Finding something wrong and sending an alert? Not that tough. But introducing things like escalations, flap detection, check intervals, notification intervals, and any number of other things you can find in such things as Nagios are non-trivial to implement, and take away from more important tasks. Ok, so why not just use nagios, or something like it. Well, you can! But setting nagios up is non-trivial, especially for a developer who's not otherwise inclined to do ops stuff, and with nagios comes lots of stuff you maybe don't want.

Alertsd attempts to make the distinction between monitoring, alerting, and notifications. In the ever-increasing world of devops this is becoming a critical distinction. Monitoring is something developers and devops people can do really well. Good monitoring requires intimate understanding of the system you're trying to monitor, whether it's CPU temperature or some metric within a java application. Notifications is something pagerduty (and things like pagerduty) does really well. They take the hassle out of sending email, making phone calls and SMS, and doing team escalations. Alertsd fits between these two things, and adds certain features that are difficult to implement in a monitoring system, especially if it's stateless (like a cron script).

Another benefit of something like this is it gives you an escalation proxy, so instead of having a bunch of nodes sending email or making API calls to pagerduty, you can do all that from here. Your firewall will thank you.

## Trying it out

To try this out, you'll need Python-Django, RabbitMQ and celery. Once you've installed those things, started your rabbitmq daemon and cloned this repo, run ```python manage.py syncdb```. You can then run the dev server with ```python manage.py runserver 0.0.0.0:8000```. To start your celery worker, run ```celery -A alertsd worker -l info```.

Assuming all of that worked, you can create some data in your db by running ```./create_db.sh```. Then to play around with triggering and resolving incidents, run ```./trigger.sh``` and ```./resolve.sh```.

## Installing

When you're done trying it out, you can take a few steps to install it in a more productized way. Have a look at the included [install.sh](install.sh). You will need RabbitMQ, Celeryd, Supervisor, Nginx, Gunicorn and Django. If you've got all that stuff installed, then you should be able to simply run the install script. 

Running these commands should result in a running alertsd instance on your vanilla ubuntu 14 box:
```
sudo apt-get install -y git-core
git clone https://github.com/afrank/alertsd.git
cd alertsd
sudo ./install.sh
```

## How do I use this glorious tool?!

Once you've installed alertsd, by either using the "trying it out" method or the "installing" method, you need to send some data to it. You can put some sample data in it by using the [create_db.sh](create_db.sh) script, but let's discuss what's happening here, so you can form these calls to meet your needs. 

### Create a user

By design, this api endpoint can only be queried from localhost. This is because alertsd (currently) has no concept of a superuser, so superuser commands are run from localhost. A user is a top-level model; the only required argument is an api key, which is just a string that could be virtually anything (though I like using uuids). So you could do something like:
```
api_key=$(uuidgen)
curl -s -X POST -d "{\"api_key\":\"$api_key\"}" $base_url/api/user/ | python -m json.tool
```

### Create an alert
```
curl -s -X POST -H "Auth-Token: $api_key" -d '{"key":"testing.key","plugin_id":1,"failure_time":300,"max_failures":5,"failure_expiration":60}' $base_url/api/alert/ | python -m json.tool
```

## Plugins
Plugins dictate the way escalations are handled. When an incident is escalated based on the alert rules, the plugin is executed as a sub-process with various things passed to it as environment variables. Using the sub-process with environment variables means plugins can be written in any scripting language.

```python manage.py syncplugins```


