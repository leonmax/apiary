'''
Created on Oct 26, 2012

@author: Yangming
'''

import settings
from rest import Rest

class ServerTags(Rest):
    '''
    classdocs
    '''

    def __init__(self):
        self.set_endpoint(settings.endpoint)
        self.set_credential(settings.credential[0], settings.credential[1])
        self.set_auth_type("basic")

    @property
    def attributes(self):
        return {"id"            : "Unique server tag id",
                "name"          : "The name of the server tag",
                "servers"       : "IDs of servers belong to this server tag",
                "resource_uri"  : "The URI to get more information about this item"
               }

    @Rest.api
    def list_servertags(self, *args):
        respJson = self.get("/server_tags/").json
        return self.filter_list_dict(respJson, *args)

    @Rest.api
    def view_servertag(self, tag_id):
        path = self.make_path("/server_tags/$tag_id", tag_id=tag_id)
        respJson = self.get(path).json
        return respJson

    @Rest.api
    def list_servertag_servers(self, *server_tags):
        """ call list_servertag_servers server_tags1 server_tags2 ...
            sample: call list_servertag_servers Redis Queue"""
        kwargs = {"server_tags":stag for stag in server_tags}
        qstr=self.make_querystring(**kwargs)
        path = self.make_path("/server_tags/servers/$qstr", qstr=qstr)
        respJson = self.get(path).json
        return respJson

    @Rest.api
    def list_servertags_versions(self):
        path = self.make_path("/server_tags/versions")
        respJson = self.get(path).json
        return respJson
