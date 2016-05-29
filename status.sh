#!/bin/bash

echo Users
curl -s -X GET -H "Auth-Token: 8725FFD7-64A1-4901-B1EA-1DC4D0340637" http://localhost:8080/api/user/ | python -m json.tool
echo Alerts
curl -s -X GET -H "Auth-Token: 8725FFD7-64A1-4901-B1EA-1DC4D0340637" http://localhost:8080/api/alert/ | python -m json.tool
echo Incidents
curl -s -X GET -H "Auth-Token: 8725FFD7-64A1-4901-B1EA-1DC4D0340637" http://localhost:8080/api/incident/ | python -m json.tool
