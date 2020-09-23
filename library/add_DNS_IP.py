#!/usr/bin/python3.8

import requests
import json
import xmltodict
from ansible.module_utils.basic import *

"""
Desc: Function to convert List of strings to a string with a separator
"""
def converttostr(input_seq, seperator):
   # Join all the strings in list
   final_str = seperator.join(input_seq)
   return final_str


def main():
  fields = {
		"Read_from_file": {"required": False, "type": "bool"},
    "DNS": {"required": False, "type": "list"},
    "IP": {"required": False, "type": "list"},
    "edit": {"required": False, "type": "bool"},
    "Authorization": {"required": True, "type": "str"},
    "QUALYS_ASSET_ID": {"required": True, "type": "str"},
    "QUALYS_API_URL": {"required": True, "type": "str"}        
	}  
        
  module = AnsibleModule(argument_spec=fields)
  Authorization = module.params['Authorization']
  QUALYS_ASSET_ID = module.params['QUALYS_ASSET_ID'] 
  QUALYS_API_URL = module.params['QUALYS_API_URL']
  
  url = QUALYS_API_URL + "/fo/asset/group/?action=edit"

  DNS = module.params['DNS']
  IP = module.params['IP']
  edit = module.params['edit']

  #Input = DNS + IP

  if not edit:
      module.exit_json(ignored=True, meta="edit variable set to False")
  seperator = ','
  dns_payload = ""
  ip_payload = ""

  if DNS:
      DNS_string = converttostr(DNS, seperator)
      dns_payload = "&add_dns_names=" + DNS_string
  elif IP:
      IP_string = converttostr(IP, seperator)
      ip_payload = "&add_ips=" + IP_string

  payload = "id=" + QUALYS_ASSET_ID + dns_payload + ip_payload
  headers = {
  'X-Requested-With': 'Ansible',  
  'Authorization': Authorization,
  'Content-Type': 'application/x-www-form-urlencoded'
  }
  
  response = requests.request("POST", url, headers=headers, data = payload)  
  data_dict = xmltodict.parse(response.text.encode('utf8'))
  Output = data_dict['SIMPLE_RETURN']['RESPONSE']['TEXT']
  
  MSG = []  
  MSG.append(Output)
  if DNS != [""]: MSG.append(DNS)
  if IP != [""]: MSG.append(IP)

  if Output == "Asset Group Updated Successfully":
        module.exit_json(changed=True, meta=MSG)  
  else:  module.exit_json(failed=True, meta=Output)     
  
if __name__ == '__main__':
    main()