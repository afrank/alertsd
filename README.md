# alertsd
A statsd-like concept for alerts

Doing alerts right is kinda hard. In the glorious world of devops, you want to do adhoc alerting, where you've got a few different products all implementing their own alerting rules, tied in to any number of things. Finding something wrong and sending an alert? Not that tough. But introducing things like escalations, flap detection, check intervals, notification intervals, and any number of other things you can find in such things as Nagios are non-trivial to implement, and take away from more important tasks. Ok, so why not just use nagios, or something like it. Well, you can! But then you get lots of stuff you don't necessarily want. If all you want is a REST API that handles various alerting intervals, escalations, and notification integrations (with things like, oh, say, pagerduty), then look no further.

Another benefit of something like this is it gives you an escalation proxy, so instead of having a bunch of nodes sending email or making API calls to pagerduty, you can do all that from here. Your firewall will thank you.
