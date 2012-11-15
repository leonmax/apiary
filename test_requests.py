'''
Created on Nov 7, 2012

@author: appfirst
'''

from pprint import pprint
import sys
sys.path = filter(lambda m: "backend" not in m, sys.path)
import requests

if __name__ == '__main__':
    url = "https://wwws.appfirst.com/api/servers/11725"
    response = requests.get(url, auth=("admin@appfirst.com","491430756"))
    print response
    if hasattr(response, "json"):
        pprint(response.json)
    else:
        print "no json returned"