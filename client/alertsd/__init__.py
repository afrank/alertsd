
import requests
import json

class Alertsd:
    def __init__(self,hostname,api_key=None):
        self.hostname = hostname
        self.api_key = api_key
    def get_plugin(self,plugin):
        headers = { 'Auth-Token': self.api_key }
        url = "{0}/api/plugin/{1}/".format(self.hostname,plugin)
        return json.loads(requests.get(url,headers=headers).text)
    def get_alert(self,alert_key):
        headers = { 'Auth-Token': self.api_key }
        url = "{0}/api/alert/{1}/".format(self.hostname,alert_key)
        return json.loads(requests.get(url,headers=headers).text)
    def list_alerts(self):
        headers = { 'Auth-Token': self.api_key }
        url = "{0}/api/alert/".format(self.hostname)
        return json.loads(requests.get(url, headers=headers).text)['objects']
    def list_incidents(self):
        headers = { 'Auth-Token': self.api_key }
        url = "{0}/api/incident/".format(self.hostname)
        return json.loads(requests.get(url, headers=headers).text)['objects']
    def list_plugins(self):
        headers = { 'Auth-Token': self.api_key }
        url = "{0}/api/plugin/".format(self.hostname)
        return json.loads(requests.get(url, headers=headers).text)['objects']
    def create_user(self,api_key=None):
        if api_key is None and self.api_key is None:
            import uuid
            self.api_key = str(uuid.uuid1())
        elif self.api_key is None:
            self.api_key = api_key
        payload = { "api_key": self.api_key }
        url = "{0}/api/user/".format(self.hostname)
        self.user = json.loads(requests.post(url, json.dumps(payload)).text)
        return self.user
    def create_alert(self,alert_key,**kwargs):
        headers = { 'Auth-Token': self.api_key }
        url = "{0}/api/alert/".format(self.hostname)
        failure_time = 300
        max_failures = 5
        failure_expiration = 60
        if 'plugin' in kwargs:
            plugin = self.get_plugin(kwargs['plugin'])
            plugin_id = plugin['id']
        if 'failure_time' in kwargs:
            failure_time = kwargs['failure_time']
        if 'max_failures' in kwargs:
            max_failures = kwargs['max_failures']
        if 'failure_expiration' in kwargs:
            failure_expiration = kwargs['failure_expiration']
        payload = { "key":alert_key,"plugin_id":plugin_id,"failure_time":failure_time,"max_failures":max_failures,"failure_expiration":failure_expiration }
        return json.loads(requests.post(url, data=json.dumps(payload), headers=headers).text)
    def add_param(self,alert_key,plugin_name,key,val):
        headers = { 'Auth-Token': self.api_key }
        url = "{0}/api/plugin_parameter/".format(self.hostname)
        alert = self.get_alert(alert_key)
        plugin = self.get_plugin(plugin_name)
        payload = { 'plugin_id': plugin['id'], 'alert_id': alert['id'], 'key':key, 'value':val }
        return json.loads(requests.post(url,data=json.dumps(payload),headers=headers).text)
    def trigger(self,alert_key,value):
        headers = { 'Auth-Token': self.api_key }
        url = "{0}/alert/".format(self.hostname)
        payload = {'key':alert_key,'action':'trigger','value':value}
        return json.loads(requests.post(url,data=payload,headers=headers).text)
    def resolve(self,alert_key,value):
        headers = { 'Auth-Token': self.api_key }
        url = "{0}/alert/".format(self.hostname)
        payload = {'key':alert_key,'action':'resolve','value':value}
        return json.loads(requests.post(url,data=payload,headers=headers).text)

