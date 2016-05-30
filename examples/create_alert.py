#!/usr/bin/python

from alertsd import Alertsd
from pprint import pprint

api_key = "7f8b419a-25bb-11e6-a813-002590eb817c"

c = Alertsd('http://localhost:8080',api_key)

pprint(c.create_alert('testing.lib', plugin='pagerduty', failure_time=300, max_failures=5, failure_expiration=60))
pprint(c.add_param('testing.lib','pagerduty','api_key','NhysDaytNvSBTEg7XCoh'))
pprint(c.add_param('testing.lib','pagerduty','service_key','d5b8864653944148a1a53695c560c92f'))
