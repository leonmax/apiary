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

    @Rest.api
    def list_processes(self, *args):
        respJson = self.get("/processes/").json
        return self.filter_list_dict(respJson, *args)

    @Rest.api
    def view_process(self, uid):
        """retrieve_processes %uid -- Retrieves historical data for the given process.
            returns process data in json"""
        path = self.make_path("/processes/$uid/data", uid=uid)
        respJson = self.get(path).json
        return respJson

    @Rest.api
    def view_process_detail(self, uid):
        path = self.make_path("/processes/$uid/detail", uid=uid)
        respJson = self.get(path).json
        return respJson

    @Rest.api
    def list_processes_versions(self):
        path = self.make_path("/processes/versions")
        respJson = self.get(path).json
        return respJson
