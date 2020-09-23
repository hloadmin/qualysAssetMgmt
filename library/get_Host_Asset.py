#!/usr/bin/python3.8

import requests
import json
import xmltodict
from ansible.module_utils.basic import *

def main():
  fields = {
		"print_full_DNS_list": {"required": True, "type": "bool"},
    "print_full_IP_list": {"required": True, "type": "bool"},
    "DNS_or_IP": {"required": True, "type": "str"},
    "Authorization": {"required": True, "type": "str"},
    "QUALYS_ASSET_ID": {"required": True, "type": "str"},    		
    "QUALYS_API_URL": {"required": True, "type": "str"}
	}  

  module = AnsibleModule(argument_spec=fields)  
  Authorization = module.params['Authorization']      
  QUALYS_ASSET_ID = module.params['QUALYS_ASSET_ID']
  QUALYS_API_URL = module.params['QUALYS_API_URL']
  
  url = QUALYS_API_URL + "/fo/asset/group/?action=list&ids=" + QUALYS_ASSET_ID +"&show_attributes=IP_SET,DNS_LIST"
  payload = {}
  headers = {
    'X-Requested-With': 'Ansible',    
    'Authorization': Authorization
  }
  DNS_or_IP = module.params['DNS_or_IP']
  print_full_DNS_list = module.params['print_full_DNS_list']
  print_full_IP_list = module.params['print_full_IP_list']
  
  response = requests.request("GET", url, headers=headers, data = payload)  
  data_dict = xmltodict.parse(response.text.encode('utf8'))
  BOTH = data_dict['ASSET_GROUP_LIST_OUTPUT']['RESPONSE']['ASSET_GROUP_LIST']['ASSET_GROUP']
  DNS_LIST = data_dict['ASSET_GROUP_LIST_OUTPUT']['RESPONSE']['ASSET_GROUP_LIST']['ASSET_GROUP']['DNS_LIST']['DNS']
  IP_RANGE = data_dict['ASSET_GROUP_LIST_OUTPUT']['RESPONSE']['ASSET_GROUP_LIST']['ASSET_GROUP']['IP_SET']['IP_RANGE']
  IP_SINGLE = data_dict['ASSET_GROUP_LIST_OUTPUT']['RESPONSE']['ASSET_GROUP_LIST']['ASSET_GROUP']['IP_SET']['IP']
  IP_LIST = IP_RANGE + IP_SINGLE
  BOTH_SHORT = "Total DNS entries " + str(len(DNS_LIST)) + " and total IP entries " + str(len(IP_LIST))
    
  if DNS_or_IP == "bothfull":
      module.exit_json(changed=False, meta=BOTH)
  elif DNS_or_IP == "bothshort":
      module.exit_json(changed=False, meta=BOTH_SHORT)
  elif DNS_or_IP == "DNS":
      if print_full_DNS_list:
          module.exit_json(changed=False, meta=DNS_LIST)
      else:
            module.exit_json(changed=False, meta=len(DNS_LIST))
  elif DNS_or_IP == "IP":
      if print_full_IP_list:
          module.exit_json(changed=False, meta=IP_LIST)
      else:
            module.exit_json(changed=False, meta=len(IP_LIST))    
  
  module.exit_json(changed=False, meta=IP_LIST)


if __name__ == '__main__':
    main()