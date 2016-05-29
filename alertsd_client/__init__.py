
import requests
import json

class Alertsd:
    def __init__(self,hostname,api_key=None):
        self.hostname = hostname
        self.api_key = api_key
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
    def list_plugins(self):
        headers = { 'Auth-Token': self.api_key }
        url = "{0}/api/plugin/".format(self.hostname)
        return json.loads(requests.get(url, headers=headers).text)['objects']
    def create_alert(self,alert_key,**kwargs):
        headers = { 'Auth-Token': self.api_key }
        url = "{0}/api/alert/".format(self.hostname)
        failure_time = 300
        max_failures = 5
        failure_expiration = 60
        if 'plugin' in kwargs:
            # lookup plugin id from string
            plugin_id = [ x['id'] for x in self.list_plugins() if x['name'] == kwargs['plugin'] ][0]
        else:
            plugin_id = kwargs['plugin_id']
        if 'failure_time' in kwargs:
            failure_time = kwargs['failure_time']
        if 'max_failures' in kwargs:
            max_failures = kwargs['max_failures']
        if 'failure_expiration' in kwargs:
            failure_expiration = kwargs['failure_expiration']
        payload = { "key":alert_key,"plugin_id":plugin_id,"failure_time":failure_time,"max_failures":max_failures,"failure_expiration":failure_expiration }
        return json.loads(requests.post(url, data=json.dumps(payload), headers=headers).text)
    def get_plugin(self,plugin):
        headers = { 'Auth-Token': self.api_key }
        url = "{0}/api/plugin/{1}/".format(self.hostname,plugin)
        return json.loads(requests.get(url,headers=headers).text)
    def get_alert(self,alert_key):
        headers = { 'Auth-Token': self.api_key }
        url = "{0}/api/alert/{1}/".format(self.hostname,alert_key)
        return json.loads(requests.get(url,headers=headers).text)
    def add_param(self,alert_key,plugin_name,key,val):
        # curl -s -X POST -H "Auth-Token: $api_key" -d '{"plugin_id":3,"alert_id":1,"key":"api_key","value":"NhysDaytNvSBTEg7XCoh"}' $base_url/api/plugin/parameter/
        headers = { 'Auth-Token': self.api_key }
        url = "{0}/api/plugin_parameter/".format(self.hostname)
        # plugin_id = [ x['id'] for x in self.list_plugins() if x['name'] == plugin ][0]
        alert = self.get_alert(alert_key)
        plugin = self.get_plugin(plugin_name)
        payload = { 'plugin_id': plugin['id'], 'alert_id': alert['id'], 'key':key, 'value':val }
        return json.loads(requests.post(url,data=json.dumps(payload),headers=headers).text)
    def trigger(self,alert_key,value):
        # curl -s -X POST -H "Auth-Token: $api_key" -d key=testing.key -d action=trigger -d value="$value" $base_url/alert/
        headers = { 'Auth-Token': self.api_key }
        url = "{0}/alert/".format(self.hostname)
        payload = {'key':alert_key,'action':'trigger','value':value}
        return json.loads(requests.post(url,data=payload,headers=headers).text)
