#!/bin/bash

curl -s -X POST -H "Auth-Token: 8725FFD7-64A1-4901-B1EA-1DC4D0340637" -d key=testing.alert_key -d action=trigger http://localhost:8000/alert/ | python -m json.tool
