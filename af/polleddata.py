'''
Created on Oct 26, 2012

@author: Yangming
'''

import settings
from rest import Rest

class PolledData(Rest):
    '''
    classdocs
    '''

    def __init__(self):
        self.set_endpoint(settings.endpoint)
        self.set_credential(settings.credential[0], settings.credential[1])
        self.set_auth_type("basic")

    @property
    def attributes(self):
        return {"id"            : "Unique id for the polled data item in our system",
                "name"          : "The name for this polled data item",
                "server"        : "The id of the server this item is running on",
                "server_uri"    : "The URI of the server this item is running on",
                "alert"         : "The id of the alert on this item",
                "alert_uri"     : "The URI for the alert on this item",
                "resource_uri"  : "The URI to get more information about this item"
               }

    def api_list_polleddata(self, *args):
        resp = self.get("/polled-data/")
        if not resp or not hasattr(resp, "json"):
            return None
        return self.filter_list_dict(resp.json, *args)

    def api_view_polleddata(self, pd_id):
        path = self.make_path("/polled-data/$pd_id/", pd_id=pd_id)
        resp = self.get(path)
        if not resp or not hasattr(resp, "json"):
            return None
        return resp.json

    def api_view_polleddata_data(self, pd_id):
        path = self.make_path("/polled-data/$pd_id/data/", pd_id=pd_id)
        resp = self.get(path)
        if not resp or not hasattr(resp, "json"):
            return None
        return resp.json

    def api_list_polleddata_versions(self):
        path = self.make_path("/polled-data/versions/")
        resp = self.get(path)
        if not resp or not hasattr(resp, "json"):
            return None
        return resp.json
