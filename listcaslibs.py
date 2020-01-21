#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# listcaslibs.py
# January 2019
#
# Usage:
# listcaslibs.py [--noheader] [-d]
#
# Examples:
#
# 1. Return list of all CAS libraries on all servers
#        ./listcaslibs.py
#
# Copyright © 2019, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the License);
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

debug=False

# Import Python modules
import argparse
import sys
from sharedfunctions import callrestapi

# Define exception handler so that we only output trace info from errors when in debug mode
def exception_handler(exception_type, exception, traceback, debug_hook=sys.excepthook):
    if debug:
        debug_hook(exception_type, exception, traceback)
    else:
        print "%s: %s" % (exception_type.__name__, exception)

sys.excepthook = exception_handler

parser = argparse.ArgumentParser()
parser.add_argument("--noheader", action='store_true', help="Do not print the header row")
parser.add_argument("-d","--debug", action='store_true', help="Debug")
args = parser.parse_args()
noheader=args.noheader
debug=args.debug

# Print header row unless noheader argument was specified
if not noheader:
    print('server,caslib')
    
endpoint='/casManagement/servers'
method='get'

#make the rest call
serverlist_result_json=callrestapi(endpoint,method)

if debug:
    print(serverlist_result_json)
    print('serverlist_result_json is a '+type(serverlist_result_json).__name__+' object') #serverlist_result_json is a dict object

servers = serverlist_result_json['items']

for server in servers:
    servername=server['name']

    # List the caslibs in this server
    endpoint='/casManagement/servers/'+servername+'/caslibs?excludeItemLinks=true&limit=10000'
    method='get'
    caslibs_result_json=callrestapi(endpoint,method)
    if debug:
        print(caslibs_result_json)
        print('caslibs_result_json is a '+type(caslibs_result_json).__name__+' object') #caslibs_result_json is a dict object
    caslibs=caslibs_result_json['items']

    for caslib in caslibs:
        print(server['name']+','+caslib['name'])
