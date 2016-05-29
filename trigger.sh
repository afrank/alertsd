#!/bin/bash

api_key="8725FFD7-64A1-4901-B1EA-1DC4D0340637"
base_url="http://localhost:8080"

value=$1

curl -s -X POST -H "Auth-Token: $api_key" -d key=escalation.email -d action=trigger -d value="$value" $base_url/alert/ | python -m json.tool
