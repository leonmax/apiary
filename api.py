#!/usr/bin/env python
# encoding: utf-8
'''
api -- 'apriarist main process entrance

api is a process entrance for apiarist for both interactive mode and command-line mode.

It defines the main entrance for apiarist

@author:     Yangming Huang

@copyright:  2012 AppFirst Inc. All rights reserved.

@license:    Apache License

@contact:    yangming@appfirst.com
@deffield    updated: Updated
'''

import config

import os
import cmd
import pprint
import traceback
import inspect
import rest

class Apiary(cmd.Cmd):
    prompt = '> '
    intro = "Apiarist, the one plays with api swarm, present to you by AppFirst"

    def __init__(self, *args, **kwargs):
        cmd.Cmd.__init__(self, *args, **kwargs)

        self.mode_stack = []
        self.all_mod = {}
        self.all_api = {}
        self.preload();
        self.last_result = None;

    def preload(self):
        for mod in config.preload_mods:
            self._load(mod)

    def _load(self, mod_name):
        if mod_name in self.all_mod:
            service = reload(self.all_mod[mod_name])
            self.all_mod[mod_name] = service
        else:
            try:
                service = __import__(mod_name, fromlist=["*"])
                self.all_mod[mod_name] = service
            except ImportError as e:
                print e
                return
        for _, membercls in inspect.getmembers(service, predicate=inspect.isclass):
            if (issubclass(membercls, rest.Rest)
                    and membercls is not rest.Rest):
                print "loading: %s" % membercls
                restobj = membercls()

                for name, memberfn in inspect.getmembers(membercls, predicate=inspect.ismethod):
                    if ("api_" in name):
                        fname = memberfn.func_name[4:]
                        self.all_api[fname] = restobj.make_command(memberfn)

    def do_load(self, line):
        for mod_name in line.split():
            self._load(mod_name)

    def do_call(self, line):
        if not line:
#            self._enter_mode("call")
            return
        argv = line.split()
        api = argv[0]
        try:
            if api and api in self.all_api:
                result = self.all_api[api](*argv[1:])
            else:
                print("api does not exist")
                return
            if not result:
                pass
            elif type(result)==str:
                print "help: %s" % result
            else:
                self.last_result = result
                if isinstance(result, str) or isinstance(result, unicode):
                    print result
                else:
                    pprint.pprint(result)
        except TypeError as e:
            print e.message
        except Exception:
            traceback.print_exc()

    def complete_call(self, text, line, begidx, endidx):
        argv = line.split()[1:]
        api = argv[0] if len(argv) > 0 else ""
        keys = self.all_api.keys()
        if not api:
            completions = keys[:]
        else:
            completions = [ f for f in keys
                            if f.startswith(api) ]
        return completions

    def do_shell(self, line):
        if not line:
#            self._enter_mode("shell")
            return
        "Run a shell command"
        print "running shell command:", line
        output = os.popen(line).read()
        print output.strip()
        self.last_result = output

    def do_replay(self, line):
        if line:
            try:
                f = open(line, "w+")
                f.write(str(self.last_result))
            except IOError:
                print 'No file found'
        pprint.pprint(self.last_result)

    def do_clear(self, line):
        if os.name == 'posix':
            os.system('clear')
        elif os == 'Windows':
            os.system('cls')

    def do_exit(self, line):
        return True

    def do_EOF(self, line):
        return True

    def default(self, line):
        try:
            d = dict(locals(), **globals())
            exec(line, d, d)
            for k in d:
                if k not in globals() and k not in locals():
                    globals()[k] = d[k]
                    print d[k]
        except Exception:
            traceback.print_exc()

#    def _enter_mode(self, mode):
#        if mode:
#            Apiary.prompt = "%s>" % mode
#            self.mode_stack.append(mode)
#
#    def onecmd(self, line):
#        if len(self.mode_stack)>0:
#            line = "%s %s" % (" ".join(self.mode_stack), line)
#        cmd.Cmd.onecmd(self, line)
#
#    def _exit_mode(self):
#        if len(self.mode_stack)>0:
#            self.mode_stack.pop()
#            if len(self.mode_stack)>0:
#                Apiary.prompt = "%s>" % self.mode_stack.pop()
#            else:
#                Apiary.prompt = ">"

    def emptyline(self):
#        self._exit_mode()
        return

if __name__ == "__main__":
    Apiary().cmdloop()