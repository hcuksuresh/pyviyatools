#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# listdomains.py
# February 2020
#
# Usage:
# listdomains.py [--noheader] [--showall] [-d]
#
# Change History
#
#  20FEB2020 Created 
#
# Examples:
#
# 1. Return list of domains that are displayed in the Domains page in SAS Environment Manager
#        ./listdomains.py
#
# Copyright © 2020, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
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
parser.add_argument("-a","--showall", action='store_true', help="Show all domains, including credentials and tokens which are not displayed in SAS Environment Manager")
parser.add_argument("-d","--debug", action='store_true', help="Debug")
args = parser.parse_args()
noheader=args.noheader
showall=args.showall
debug=args.debug

# Print header row unless noheader argument was specified
if not noheader:
    print('id,type,description')
    
endpoint='/credentials/domains?limit=10000'
method='get'

#make the rest call
domainlist_result_json=callrestapi(endpoint,method)

normalDomainTypes=['password','connection','cryptDomain']

if debug:
    print(domainlist_result_json)
    print('domainlist_result_json is a '+type(domainlist_result_json).__name__+' object') #domainlist_result_json is a dict object

domains = domainlist_result_json['items']

for domain in domains:
    id=domain['id']
    type=domain['type']
    description=domain['description']

    if type in normalDomainTypes or showall:
        print(id+","+type+",\""+description+"\"")
