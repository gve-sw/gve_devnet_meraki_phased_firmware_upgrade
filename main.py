""" Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

#Imports
import os
import requests
import json
from dotenv import load_dotenv

#Environment Variables
load_dotenv()
MERAKI_BASE_URL = os.environ['MERAKI_BASE_URL']
NETWORK_NAME = os.environ['NETWORK_NAME']
ORG_NAME = os.environ['ORG_NAME']

#Headers
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Cisco-Meraki-API-Key": os.environ['API_KEY']
}

#Get the ID of the targeted organization
def get_organizations_names_ids():
    try:
        organizations = requests.get(MERAKI_BASE_URL+'/organizations', headers=headers).json()
        for org in organizations:
            if org["name"]==ORG_NAME:
                org_id=org["id"]
                network_id=get_networks_ids_names(org_id)
                return network_id
    except Exception as e:
            print("Exception in get_organizations_names_ids: " + str(e))

#Get the ID of the targeted network
def get_networks_ids_names(org_id):
    try:
        url = MERAKI_BASE_URL+ f"/organizations/{org_id}/networks"
        networks = requests.get(url, headers=headers).json()
        for network in networks:
            if network["name"]==NETWORK_NAME:
                network_id=network["id"]
                return network_id
    except Exception as e:
            print("Exception in get_networks_ids_names: " + str(e))

#Get all devices in the targeted network
def get_network_devices(network_id):
    try:
        url= MERAKI_BASE_URL + f"/networks/{network_id}/devices"
        devices = requests.get(url,headers=headers).json()
        return devices
    except Exception as e:
            print("Exception in get_network_devices: " + str(e))

#Get the names and IDs of switch stacks in the targeted network
def get_switch_stacks(networkId):
    try:
        url= MERAKI_BASE_URL + f"/networks/{networkId}/switch/stacks"
        stacks=requests.get(url, headers=headers).json()

        stacks_list=[]
        
        for stack in stacks:
            stack_entry={}
            stack_entry["name"]=stack["name"]
            stack_entry["id"]=stack["id"]
            stacks_list.append(stack_entry)

        return stacks_list
    except Exception as e:
            print("Exception in get_switch_stacks: " + str(e))

#Create a network firmware upgrades staged group
#This is for core and access switches
def create_group(network_id, serials, group_name):
    try:
        url= MERAKI_BASE_URL + f"/networks/{network_id}/firmwareUpgrades/staged/groups"

        if len(serials) == 1:
            payload={}
            payload["name"]= group_name
            payload["isDefault"]=False
            payload["assignedDevices"]={
                        "devices": [
                            {
                                "serial": serials[0]
                                
                            }
                        ]
                    }

        
            groups=  requests.post(url, headers=headers, data=json.dumps(payload)).json()
            print(json.dumps(groups, indent=2))
            group_id=groups["groupId"]
            return group_id
        
        else: 
            payload={}
            payload["name"]= group_name
            payload["isDefault"]=False
            payload["assignedDevices"]={
                                "devices": [
                                ]
                            }
            n= 0

            for s in serials:

                if n <= len(serials)-1:
                    entry={"serial": s}
                    payload["assignedDevices"]["devices"].append(entry)
                    n+=1
            
        
            groups=  requests.post(url, headers=headers, data=json.dumps(payload)).json()
            print(json.dumps(groups, indent=2))
            group_id=groups["groupId"]
            return group_id
    except Exception as e:
            print("Exception in create_group: " + str(e))

#Create a network firmware upgrades staged group
#This is for the switch stacks
def create_group_stacks(network_id, stacks):
    try:
        url= MERAKI_BASE_URL + f"/networks/{network_id}/firmwareUpgrades/staged/groups"
        groups_ids=[]

        for stack in stacks:
            payload={}
            payload["name"]= "Group for Stack: "+ stack["name"]
            payload["isDefault"]=False
            payload["assignedDevices"]={

            }

            s=[{
                "name":stack["name"],
                "id":stack["id"]
            }]
            payload["assignedDevices"]["switchStacks"]=s

            groups= requests.post(url, headers=headers, data=json.dumps(payload)).json()
            group_id=groups["groupId"]
            groups_ids.append(group_id)
    
        return groups_ids
    except Exception as e:
            print("Exception in create_group_stacks: " + str(e))
    
#Get the all the configured network firmware upgrades staged groups
def get_all_groups(networkId):
    try:
        url= MERAKI_BASE_URL + f"/networks/{networkId}/firmwareUpgrades/staged/groups"
        upgrade_groups= requests.get(url, headers=headers).json()
        groups_ids=[]
        for group in upgrade_groups:
            groups_ids.append(group["groupId"])
        return groups_ids
    except Exception as e:
            print("Exception in get_all_groups: " + str(e))
    
#Get the available firmware upgrades        
def get_network_upgrades(networkId):
    try:
        url= MERAKI_BASE_URL + f"/networks/{networkId}/firmwareUpgrades"
        available_upgrades=requests.get(url, headers=headers).json()
        switch_upgrades=available_upgrades["products"]["switch"]["availableVersions"]
        for stable_upgrade in switch_upgrades:
            if stable_upgrade["releaseType"] == "stable":
                upgrade_id=stable_upgrade["id"]
                print(upgrade_id)
        return upgrade_id
    except Exception as e:
            print("Exception in get_network_upgrades: " + str(e))
    
#Create network firmware upgrades staged event
def schedule_upgrade(networkId, upgrade_id, core_switches_group_id, access_switches_group_id, core_schedule, access_schedule, groups_ids,other_groups_schedule):
    try:
        url= MERAKI_BASE_URL + f"/networks/{networkId}/firmwareUpgrades/staged/events"
        payload={
                "products": {
                    "switch": {
                        "nextUpgrade": {
                            "toVersion": { "id": "" }
                        }
                    },
                    "switchCatalyst": {
                    
                    }
                },
                "stages": [
                    {
                        "group": { "id": "" },
                        "milestones": {
                            "scheduledFor": ""
                        }
                    },
                    {
                        "group": { "id": "" },
                        "milestones": {
                            "scheduledFor": ""
                        }
                    }

                ]
            }

        payload["products"]["switch"]["nextUpgrade"]["toVersion"]["id"]=upgrade_id

        payload["stages"][0]["group"]["id"]=access_switches_group_id
        payload["stages"][0]["milestones"]["scheduledFor"]=access_schedule

        payload["stages"][1]["group"]["id"]=core_switches_group_id
        payload["stages"][1]["milestones"]["scheduledFor"]=core_schedule

        if groups_ids != []:
            for id in groups_ids:
                entry={
                    "group":{
                        "id":id
                            },
                    "milestones": {
                            "scheduledFor": other_groups_schedule
                            }
                    }
                payload["stages"].append(entry)
                
        
        sceduel_upgrade= requests.post(url, headers=headers, data=json.dumps(payload)).json()
        print(json.dumps(sceduel_upgrade, indent=2))
    except Exception as e:
            print("Exception in schedule_upgrade: " + str(e))

#Get the network wireless settings and check the upgrade strategy
def get_wireless_settings(networkId):
    try:
        url= MERAKI_BASE_URL + f"/networks/{networkId}/wireless/settings"
        current_settings=requests.get(url, headers=headers).json()
        if current_settings["upgradeStrategy"] != "minimizeClientDowntime":
            update_wireless_settings(networkId)
    except Exception as e:
            print("Exception in get_wireless_settings: " + str(e))

#Set the upgrade strategy to 'minimizeClientDowntime'
def update_wireless_settings(networkId):
    try:
        url= MERAKI_BASE_URL + f"/networks/{networkId}/wireless/settings"
        payload={
            "upgradeStrategy": "minimizeClientDowntime",
            }
        updated_settings=requests.put(url, headers=headers,data=json.dumps(payload)).json()
        #Verify the change
        get_wireless_settings(networkId)
    except Exception as e:
            print("Exception in update_wireless_settings: " + str(e))
    
#Main function
def main():
    access_switches=[]
    core_switches=[]
    
    NETWORK_ID=get_organizations_names_ids()

    devices=get_network_devices(NETWORK_ID)
            
    for device in devices:
        if "MS" in device["model"]:
            if device["notes"]=="Core Switch":
                core_switches.append(device["serial"])
            elif device["notes"]=="Access-Switch":
                access_switches.append(device["serial"])

    core_switches_group_id=create_group(NETWORK_ID, core_switches, "Group for CORE Switches")
    access_switches_group_id=create_group(NETWORK_ID, access_switches, "Group for ACCESS Switches")

    stacks=get_switch_stacks(NETWORK_ID)
    stacks_groups=create_group_stacks(NETWORK_ID, stacks)
    
    groups_ids=get_all_groups(NETWORK_ID)
    
    groups_ids.remove(core_switches_group_id)
    groups_ids.remove(access_switches_group_id)
    
    upgrade_id=get_network_upgrades(NETWORK_ID)

    access_schedule="2023-09-30T00:00:00Z"
    core_schedule="2023-10-05T00:00:00Z"
    other_groups_schedule="2023-10-15T00:00:00Z"

    schedule_upgrade(NETWORK_ID, upgrade_id, core_switches_group_id, access_switches_group_id, core_schedule, access_schedule, groups_ids,other_groups_schedule)

    get_wireless_settings(NETWORK_ID)
    
if __name__ == '__main__':
   main()