# alertsd
A statsd-like concept for alerts

Doing alerts right is kinda hard. In the glorious world of devops, you want to do adhoc alerting, where you've got a few different products all implementing their own alerting rules, tied in to any number of things. Finding something wrong and sending an alert? Not that tough. But introducing things like escalations, flap detection, check intervals, notification intervals, and any number of other things you can find in such things as Nagios are non-trivial to implement, and take away from more important tasks. Ok, so why not just use nagios, or something like it. Well, you can! But setting nagios up is non-trivial, especially for a developer who's not otherwise inclined to do ops stuff, and with nagios comes lots of stuff you maybe don't want.

Alertsd attempts to make the distinction between monitoring, alerting, and notifications. In the ever-increasing world of devops this is becoming a critical distinction. Monitoring is something developers and devops people can do really well. Good monitoring requires intimate understanding of the system you're trying to monitor, whether it's CPU temperature or some metric within a java application. Notifications is something pagerduty (and things like pagerduty) does really well. They take the hassle out of sending email, making phone calls and SMS, and doing team escalations. Alertsd fits between these two things, and adds certain features that are difficult to implement in a monitoring system, especially if it's stateless (like a cron script).

Another benefit of something like this is it gives you an escalation proxy, so instead of having a bunch of nodes sending email or making API calls to pagerduty, you can do all that from here. Your firewall will thank you.

## Trying it out

To try this out, you'll need Python-Django, RabbitMQ and celery. Once you've installed those things, started your rabbitmq daemon and cloned this repo, run ```python manage.py syncdb```. You can then run the dev server with ```python manage.py runserver 0.0.0.0:8000```. To start your celery worker, run ```celery -A alertsd worker -l info```.

Assuming all of that worked, you can create some data in your db by running ```./create_db.sh```. Then to play around with triggering and resolving incidents, run ```./trigger.sh``` and ```./resolve.sh```.

