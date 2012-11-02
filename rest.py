'''
Created on Oct 26, 2012

@author: Yangming Huang
'''

from string import Template
import requests
import sys
import inspect
sys.path = filter(lambda m: "backend" not in m, sys.path)

class Rest(object):
    '''
    classdocs
    '''
    @classmethod
    def api(cls, fn):
        if not hasattr(cls, "commands"):
            cls.commands = []
        cls.commands.append(fn)
        return fn

    def make_command(self, fn):
        argspec = inspect.getargspec(fn)
        def self_fn(*args):
            argcount = fn.func_code.co_argcount
            if argcount > len(args)+1 and fn.__doc__:
                return fn.__doc__
            if argspec.varargs:
                return fn(self, *args)
            else:
                return fn(self, *args[:argcount-1])
        return self_fn;

    def __init__(self):
        self.auth_type = None
        self.fmt = None

    def set_endpoint(self, endpoint):
        self.endpoint = endpoint

    def set_credential(self, api_id, api_key):
        self.api_id = api_id
        self.api_key = api_key

    def set_auth_type(self, auth_type):
        self.auth_type = auth_type

    def set_head(self, head={}):
        pass

    def make_auth(self, method, path, head={}, data=None):
        if self.auth_type == "basic":
            return (self.api_id, self.api_key)

    def make_querystring(self, **kwargs):
        qstr = ""
        for k, v in kwargs.iteritems():
            if qstr:
                qstr += "&"
            else:
                qstr = "?"
            import re
            v = re.sub(r"\s+", r"+", v)
            qstr += "%s=%s" % (k,v)
        return qstr

    def make_path(self, path_fmt, **kwargs):
        fmt = Template(path_fmt)
        path = fmt.safe_substitute(**kwargs)
        return path

    def make_url(self, path):
        url = self.endpoint + path
        return url

    def filter_list_dict(self, json, *fields):
        if fields:
            json = map(lambda d: {k: d[k] for k in fields if k in d}, json)
        return json

    def filter_dict(self, json, *fields):
        if fields:
            json = {k: json[k] for k in fields if k in json}
        return json

    def get(self, path, head={}):
        url = self.make_url(path)
        auth = self.make_auth("GET", path)
        response = requests.get(url, auth=auth)
        return response

    def post(self, path, data=None, head={}):
        url = self.make_url(path)
        auth = self.make_auth("POST", path)
        response = requests.post(url, auth=auth)
        return response