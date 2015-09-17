#!/bin/bash

curl -s -X POST -d '{"api_key":"8725FFD7-64A1-4901-B1EA-1DC4D0340637"}' http://localhost:8000/api/user/ | python -m json.tool
curl -s -X POST -H "Auth-Token: 8725FFD7-64A1-4901-B1EA-1DC4D0340637" -d '{"user_id":1, "escalation_interval":0, "plugin":"dummy"}' http://localhost:8000/api/escalation/ | python -m json.tool
curl -s -X POST -H "Auth-Token: 8725FFD7-64A1-4901-B1EA-1DC4D0340637" -d '{"alert_key":"testing.alert_key", "escalation_id":1, "failure_time":300, "max_failures":5, "failure_expiration":60}' http://localhost:8000/api/alert/ | python -m json.tool
