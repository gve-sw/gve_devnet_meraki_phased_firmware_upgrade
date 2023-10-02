# GVE DevNet Meraki Switches Phased Upgrade 
This prototype utilizes the Meraki Dashboard APIs to schedule phased/staged firmware upgrades for Meraki MS switches allowing for more flexibility in the upgrade process. Staged Upgrades allows administrators to divide a network of switches into smaller groups which can have firmware upgraded at separate times.

Also it ensures that the upgrade strategy for Meraki Access Pointes APs is set to 'minimizeClientDowntime'. This option helps minimize client downtime when a wireless network upgrades/downgrades the firmware.  

## Contacts
* Roaa Alkhalaf

## Solution Components
* Meraki Dashboard APIs
* Python
* Meraki

## Workflow
This section will explain the step by step workflow in the order found in the `main()` function in the `main.py` script:

1. Retrieving the network ID of the targeted network; then retrieving all the devices within that network.
2. Filtering out the MS switches and creating two network firmware upgrades staged groups (core switches and access switches) based on the device notes. 
3. Retrieving the switch stacks in the network and create a network firmware upgrades staged group for each stack. 
4. Retrieving the IDs of all the configured network firmware upgrades staged groups.
5. Retrieving the available upgrades for MS switches. Here the stable version is used. 
6. The three variables `access_schedule`, `core_schedule` and `other_groups_schedule` are used to specify the upgrade time and date.(In ISO-8601 format, in the time zone of the network.)
7. The upgrades are then scheduled based on the above three variables.
8. The `get_wireless_settings()` function checks the configured upgrade strategy for access points; and configures it as 'minimizeClientDowntime' if not configured already. 

## Notes
1. The code assumes that groups are not created already. A functionality to check if a group needs to be updated can be added.
2. If a switch is not added to a group, it'll be part of the default group.
3. The code targets MS switches only and not Catalyst. 
4. In `schedule_upgrade()` function, all the configured network firmware upgrades staged groups should be part of the payload. 


## Installation/Configuration

The following commands are executed in the terminal.

1. Make sure Python 3 is installed in your environment, and if not, you may download Python [here](https://www.python.org/downloads/). 

2. (Optional) Set up a Python virtual environment. Once Python 3 is installed in your environment, you can activate the virtual environment with the instructions found [here](https://docs.python.org/3/tutorial/venv.html). 

    2a. Access the created virtual environment folder

        $ cd your_venv

3. Clone this repository

        $ git clone https://wwwin-github.cisco.com/gve/gve_devnet_meraki_phased_firmware_upgrade.git

4. Access the folder `gve_devnet_meraki_phased_firmware_upgrade`

        $ cd gve_devnet_meraki_phased_firmware_upgrade

5. Install the dependencies:

        $ pip3 install -r requirements.txt

6. In `.env` file, fill out the Meraki API key and the Meraki network you're targeting:

```
MERAKI_API_KEY = 
MERAKI_BASE_URL = https://api.meraki.com/api/v1
NETWORK_NAME=
ORG_NAME=

```

## Usage
1. To test the protype, type the following command in your terminal:

        $ python3 main.py


#

# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.