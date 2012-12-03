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

    def api_application_summary_metrics(self, account_id, api_key, app_id=None):
        if app_id:
            path = self.make_path("/accounts/$account_id/applications/$app_id/threshold_values.xml$qstr",
                                  account_id=settings.account_id, app_id=app_id, qstr=qstr)
        else:
            path = "/accounts.xml?include=application_health"
        self.set_headers({"x-api-key": api_key}) 
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

    def api_get_fields(self, agent_id, *args):
        metrics = self.api_get_metrics_names(agent_id, *args)
        fields = {}
        for m in metrics:
            for f in m["fields"]:
                fields.setdefault(f, []).append(m["name"])
        return fields

    def api_get_all_metrics_data(self, agent_id):
        qPara = []
        qPara.append(("begin","2012-11-15T05:47:19Z"))
        qPara.append(("end","2012-11-15T05:52:19Z"))
        if agent_id:
            qPara.append(("agent_id[]", str(agent_id)))
        else:
            pass
#            agents = self.api_list_applications()
#            for a in agents
#                qPara.append("agent_id[]", a)
        metrics = self.api_get_metrics_names(agent_id)
        for m in metrics:
            qPara.append(("metrics[]", m["name"]))
        for f in self.api_get_fields(agent_id).keys():
            qPara.append(("field", f))
        qPara.append(("summary", "1"))

        qstr = self._convert_query_string(qPara)
        path = self.make_path("/api/v1/accounts/$account_id/metrics/data.$format$qstr",
                               account_id=settings.account_id, format="json", qstr=qstr)
        print path
        resp = self.get(path)
        return resp.json

    def _convert_query_string(self, qPara):
        qstr = ""
        for k, v in qPara:
            if qstr:
                qstr += "&"
            else:
                qstr = "?"
            import re
            v = re.sub(r"\s+", r"+", v)
            qstr += "%s=%s" % (k,v)
        return qstr
