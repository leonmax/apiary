'''
Created on Nov 13, 2012

@author: appfirst
'''

import settings
from rest import Rest

class Account(Rest):
    '''
    classdocs
    '''

    def __init__(self):
        self.set_endpoint(settings.endpoint)
#        self.set_credential(settings.credential[0], settings.credential[1])
#        self.set_auth_type("basic")
        self.set_headers(settings.headers)

    def api_list_servers(self, *args):
        path = self.make_path("/api/v1/accounts/$account_id/servers.xml",
                              account_id=settings.account_id)
        resp = self.get(path)
        return resp.text

    def api_list_applications(self, *args):
        path = self.make_path("/accounts/$account_id/applications.xml",
                              account_id=settings.account_id)
        resp = self.get(path)
        return resp.text

    def api_list_hosts(self, app_id):
        path = self.make_path("/api/v1/accounts/:account_id/applications/:app_id/hosts.xml",
                              account_id=settings.account_id, app_id=app_id)
        resp = self.get(path)
        return resp.text

    def api_get_metrics_names(self, agent_id, *args):
        path = self.make_path("/api/v1/agents/$agent_id/metrics.$format", agent_id=agent_id, format="json")
        resp = self.get(path)
        return self.filter_list_dict(resp.json, *args)

    def api_get_metrics_data(self, agent_id=None):
        if agent_id:
            path = self.make_path("/api/v1/accounts/$account_id/agents/$agent_id/data.$format",
                              account_id=settings.account_id, agent_id=agent_id, format="json")
        else:
            path = self.make_path("/api/v1/accounts/$account_id/metrics/data.$format",
                              account_id=settings.account_id, format="json")
        resp = self.get(path)
        return resp.json
