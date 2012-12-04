'''
Created on Oct 26, 2012

@author: Yangming
'''

import settings
from rest import Rest

class Processes(Rest):
    '''
    classdocs
    '''

    def __init__(self):
        self.set_endpoint(settings.endpoint)
        self.set_credential(settings.credential[0], settings.credential[1])
        self.set_auth_type("basic")

    @property
    def attributes(self):
        return {}

    def api_list_processes(self, *args):
        resp = self.get("/processes/")
        if not resp or not hasattr(resp, "json"):
            return None
        return self.filter_list_dict(resp.json, *args)

    def api_view_process(self, uid):
        """retrieve_processes %uid -- Retrieves historical data for the given process.
            returns process data in json"""
        path = self.make_path("/processes/$uid/data", uid=uid)
        resp = self.get(path)
        if not resp or not hasattr(resp, "json"):
            return None
        return resp.json

    def api_view_process_detail(self, uid):
        path = self.make_path("/processes/$uid/detail", uid=uid)
        resp = self.get(path)
        if not resp or not hasattr(resp, "json"):
            return None
        return resp.json

    def api_list_processes_versions(self):
        path = self.make_path("/processes/versions")
        resp = self.get(path)
        if not resp or not hasattr(resp, "json"):
            return None
        return resp.json
