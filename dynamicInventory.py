#!/usr/bin/python3
import sys
import json
import os

IPs = sys.argv[1:]
ip_list_ul = []

for ip in IPs:
    second_octate = int(ip.split('.')[1][:])
    if (second_octate == 64) or (second_octate == 65) or (second_octate == 150) or (
            second_octate == 147) or (second_octate == 100) or (second_octate == 146) or (second_octate == 151):
        ip_list_ul.append(ip)

null = None
data = dict()
mac_host = dict()
mac_children = dict()
ul_atl = dict()
hosts = dict()
host_vars = dict()
all_vars = dict()

# UL atlanta
hosts = dict()
for ip in ip_list_ul:
    hosts[ip] = null
ul_atl["hosts"] = hosts
host_vars = dict()
host_vars["ansible_ssh_pass"] = "{{ password }}"
host_vars["ansible_become_pass"] = "{{ password }}"
host_vars["kcpassword"] = "kcpassword"
ul_atl["vars"] = host_vars

mac_children["ul_atl"] = ul_atl

mac_host["children"] = mac_children

all_vars["ansible_user"] = "uladmin"
all_vars["ansible_connection"] = "ssh"
all_vars["ansible_become"] = "yes"
all_vars["ansible_become_method"] = "sudo"
all_vars["ansible_python_interpreter"] = "/usr/bin/python3"
all_vars["ansible_ssh_common_args"] = "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

mac_host["vars"] = all_vars

data["ul-servers"] = mac_host

json_object = json.dumps(data, indent=2)

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(root_path)
file_path = os.path.join(root_path, 'playbook/inventory.json')
with open(file_path, "w") as outfile:
    outfile.write(json_object)
