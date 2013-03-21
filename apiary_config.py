'''
Created on Nov 1, 2012

@author: Yangmign Huang
'''

def config_path():
    import sys
    sys.path = filter(lambda m: m and "backend" not in m, sys.path)
#    import os
    #for d in os.listdir("."):
    #    sys.path.append(d)


config_path()

preload_mods = ["nr.account"
#               ,"af.polleddata"
#               ,"af.servers"
#               ,"af.processes"
#               ,"af.servertags"
               ]
