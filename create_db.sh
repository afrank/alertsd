#!/bin/bash

api_key="8725FFD7-64A1-4901-B1EA-1DC4D0340637"
base_url="http://localhost:8000"

curl -s -X POST -d "{\"api_key\":\"$api_key\"}" $base_url/api/user/ | python -m json.tool
curl -s -X POST -H "Auth-Token: $api_key" -d '{"user_id":1,"escalation_interval":0,"plugin_id":1}' $base_url/api/escalation/ | python -m json.tool
curl -s -X POST -H "Auth-Token: $api_key" -d '{"key":"testing.key","escalation_id":1,"failure_time":300,"max_failures":5,"failure_expiration":60}' $base_url/api/alert/ | python -m json.tool
curl -s -X POST -H "Auth-Token: $api_key" -d '{"name":"dummy","path":"dummy","required_parameters":""}' $base_url/api/plugin/ | python -m json.tool
curl -s -X POST -H "Auth-Token: $api_key" -d '{"plugin_id":1,"key":"test","value":"123"}' $base_url/api/plugin/parameter/ | python -m json.tool
