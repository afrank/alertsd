#!/bin/bash

curl -s -X GET http://localhost:8000/api/user/ | python -m json.tool
curl -s -X GET http://localhost:8000/api/escalation/ | python -m json.tool
curl -s -X GET http://localhost:8000/api/alert/ | python -m json.tool
curl -s -X GET http://localhost:8000/api/incident/ | python -m json.tool
