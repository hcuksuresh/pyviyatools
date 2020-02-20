#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# deletedomain.py
# February 2020
#
# Pass in a domain id and delete the domain, including any credentials which
# belong to that domain. See the Domains page in SAS Environment Manager, or
# use listdomains.py, to get a list of domains including the id of each
# domain. This pyviyatool can delete encryption domains, which SAS Environment
# Manager will not allow you to delete (at the time this tool was developed).
#
# Usage:
# deletedomain.py --id id [--quiet]
#
# Change History
#
#  20FEB2020 Created 
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

# Import Python modules

import argparse, sys

from sharedfunctions import callrestapi

# get python version  
version=int(str(sys.version_info[0]))

# get input parameters	
parser = argparse.ArgumentParser(description="Delete a domain and its credentials")
parser.add_argument("--id", help="id of the domain to delete.",required='True')
parser.add_argument("-f","--force", help="Force deletion, do not show an 'are you sure?' prompt.", action='store_true')
parser.add_argument("-d","--debug", action='store_true', help="Debug")
args = parser.parse_args()
id_to_delete=args.id
force=args.force
debug=args.debug

print("Looking for domain id="+id_to_delete)

# Get a list of all domains, which we will search for the domain id in the arguments.
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

    if id == id_to_delete :
        # Domain was found
        print("Found domain id: "+id+" Description: \""+description+"\"")
        
        # Prompt are you sure, unless the user specified the --force (or -f) argument
        if force:
            areyousure="Y"
        else:
            #  Deal with python 2 v python 3 prompts
            if version  > 2:
                areyousure=input("Are you sure you want to delete this domain and its credentials? (Y)")
            else:
                areyousure=raw_input("Are you sure you want to delete this domain and its credentials? (Y)") 
    
        if areyousure.upper() =='Y':
            # Delete the domain
            print("Deleting domain id: "+id+" Description: \""+description+"\"")
            reqval='/credentials/domains/'+id+'?includeCredentials=true'
            reqtype='delete'
            deletedomain_result_json=callrestapi(reqval,reqtype)
            
            if debug:
                print(deletedomain_result_json)
                print('deletedomain_result_json is a '+type(deletedomain_result_json).__name__+' object') #deletedomain_result_json is a dict object

            print('Deletion attempt complete - are any errors displayed above this line?')
        else:
            print("Exiting without deleting domain id: "+id)
