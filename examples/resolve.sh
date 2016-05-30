#!/bin/bash

api_key="8725FFD7-64A1-4901-B1EA-1DC4D0340637"
base_url="http://localhost:8000"

curl -s -X POST -H "Auth-Token: $api_key" -d key=testing.key -d action=resolve $base_url/alert/ | python -m json.tool
