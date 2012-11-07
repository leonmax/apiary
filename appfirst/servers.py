'''
Created on Oct 26, 2012

@author: Yangming
'''

import settings
from rest import Rest

class Servers(Rest):
    '''
    classdocs
    '''

    def __init__(self):
        self.set_endpoint(settings.endpoint)
        self.set_credential(settings.credential[0], settings.credential[1])
        self.set_auth_type("basic")

    @property
    def attributes(self):
        return {"id"                : "Unique server id",
                "created"           : "The time the server was created in UTC seconds",
                "os"                : "The OS for this server, either Windows or Linux.",
                "hostname"          : "The hostname for this server",
                "nickname"          : "The user-defined nickname of the server",
                "resource_uri"      : "The URI to get more information about this item",
                "running"           : "Boolean indicating whether the server is currently uploading data to AppFirst",
                "capacity_mem"      : "The total available memory on the server in bytes",
                "capacity_cpu_num"  : "The number of CPU cores on the system",
                "capacity_cpu_freq" : "The frequency of the CPU in MHz",
                "capacity_disks"    : "Mapping of the names of the disks (mount points) to their capacity in MB",
                "current_version"   : "Version of AppFirst collector that's running on the server",
                "location_ip"       : "IP Address of AppFirst collector is uploading from",
                "distribution"      : "The OS distribution e.g. Ubuntu, RedHat",
                "architecture"      : "The architecture of the server",
                "kernel_version"    : "The specific kernel version of the server's OS"
               }

    @Rest.api
    def list_servers(self, *args):
        resp = self.get("/servers/")
        if not resp or not hasattr(resp, "json"):
            return None
        return self.filter_list_dict(resp.json, *args)

    @Rest.api
    def view_server(self, server_id):
        """view_server %server_id -- returns server data in json"""
        path = self.make_path("/servers/$server_id", server_id=server_id)
        resp = self.get(path)
        if not resp or not hasattr(resp, "json"):
            return None
        return resp.json

    @Rest.api
    def view_server_data(self, server_id):
        path = self.make_path("/servers/$server_id/data", server_id=server_id)
        resp = self.get(path)
        if not resp or not hasattr(resp, "json"):
            return None
        return resp.json

    @Rest.api
    def view_server_outages(self, server_id):
        path = self.make_path("/servers/$server_id/outages", server_id=server_id)
        resp = self.get(path)
        if not resp or not hasattr(resp, "json"):
            return None
        return resp.json

    @Rest.api
    def view_server_polleddataconfig(self, server_id, *args):
        path = self.make_path("/servers/$server_id/polled_data_config", server_id=server_id)
        resp = self.get(path)
        if not resp or not hasattr(resp, "json"):
            return None
        return self.filter_dict(resp.json, *args)

    @Rest.api
    def view_server_tags(self, server_id):
        path = self.make_path("/servers/$server_id/tags", server_id=server_id)
        resp = self.get(path)
        if not resp or not hasattr(resp, "json"):
            return None
        return resp.json

    @Rest.api
    def list_server_versions(self):
        path = self.make_path("/servers/versions")
        resp = self.get(path)
        if not resp or not hasattr(resp, "json"):
            return None
        return resp.json
