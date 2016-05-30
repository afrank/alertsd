#!/usr/bin/python

from alertsd import Alertsd
from pprint import pprint

api_key = "7f8b419a-25bb-11e6-a813-002590eb817c"

c = Alertsd('http://localhost:8080',api_key)

pprint(c.create_user())

