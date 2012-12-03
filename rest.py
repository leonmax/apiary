'''
Created on Oct 26, 2012

@author: Yangming Huang
'''

from string import Template
import sys
import inspect
old_path = sys.path
sys.path = filter(lambda m: m and "backend" not in m, sys.path)
import requests
sys.path = old_path

class Rest(object):
    '''
    classdocs
    '''

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

    def set_endpoint(self, endpoint):
        self.endpoint = endpoint

    def set_credential(self, api_id, api_key):
        self.api_id = api_id
        self.api_key = api_key

    def set_auth_type(self, auth_type):
        self.auth_type = auth_type

    def set_headers(self, headers={}):
        self.headers = headers

    def make_auth(self, method, path, head={}, data=None):
        # TODO: support more auth types
        # override this function to make customed auth
        if not hasattr(self,"auth_type"):
            self.auth_type = None
        if self.auth_type == "basic":
            return (self.api_id, self.api_key)
        else:
            return None

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

    def _filter_dict(self, fields):
        def filter_dict_by_fields(d):
            newD = {}
            for k in fields:
                if k in d:
                    newD[k] = d[k]
        return filter_dict_by_fields

    def filter_list_dict(self, json, *fields):
        if fields:
            json = map(lambda d: dict([(k, d[k]) for k in fields if k in d]), json)
#            json = map(self._filter_dict(fields), json)
        return json

    def filter_dict(self, json, *fields):
        if fields:
            json = dict([(k, json[k]) for k in fields if k in json])
#            json = self._filter_dict(filter)(json)
        return json

    def get(self, path, headers={}):
        url = self.make_url(path)
        auth = self.make_auth("GET", path)
        if hasattr(self, "headers"):
            headers.update(self.headers)
        response = requests.get(url, auth=auth, headers=headers)
        return response

    def post(self, path, data=None, headers={}):
        url = self.make_url(path)
        auth = self.make_auth("POST", path)
        if hasattr(self, "headers"):
            headers.update(self.headers)
        response = requests.post(url, auth=auth, headers=headers)
        return response
