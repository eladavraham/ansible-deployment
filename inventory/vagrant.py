#!/usr/bin/env python
"""
Vagrant external inventory script. Automatically finds the IP of the booted vagrant vm(s), and
returns it under the host group 'vagrant'

Example Vagrant configuration using this script:

    config.vm.provision :ansible do |ansible|
      ansible.playbook = "./provision/your_playbook.yml"
      ansible.inventory_file = "./provision/inventory/vagrant.py"
      ansible.verbose = true
    end
"""

# Copyright (C) 2013  Mark Mandel <mark@compoundtheory.com>
#               2015  Igor Khomyakov <homyakov@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#
# Thanks to the spacewalk.py inventory script for giving me the basic structure
# of this.
#

import sys
import os.path
import subprocess
from paramiko import SSHConfig
from cStringIO import StringIO
from optparse import OptionParser
from collections import defaultdict
try:
    import json
except:
    import simplejson as json

_group = 'vagrant'  # a default group
_ssh_to_ansible = [('user', 'ansible_ssh_user'),
                   ('hostname', 'ansible_ssh_host'),
                   ('identityfile', 'ansible_ssh_private_key_file'),
                   ('port', 'ansible_ssh_port'),
                   ('python_interpreter', 'ansible_python_interpreter')]

# Options
# ------------------------------

parser = OptionParser(usage="%prog [options] --list | --host <machine>")
parser.add_option('--list', default=False, dest="list", action="store_true",
                  help="Produce a JSON consumable grouping of Vagrant servers for Ansible")
parser.add_option('--host', default=None, dest="host",
                  help="Generate additional host specific details for given host for Ansible")
(options, args) = parser.parse_args()

#
# helper functions
#


# get all the ssh configs for all boxes in an array of dictionaries.
def get_ssh_config():
    return {k: get_a_ssh_config(k) for k in list_running_boxes()}


# list all the running boxes
def list_running_boxes():
    output = subprocess.check_output(["vagrant", "global-status"]).split('\n')

    boxes = []

    for line in output[2:]:
        vbox = tuple(line.split())
        if len(vbox) == 5 and vbox[3] == "running":
            # append vagrant box: (id, name, provider, state, path)
            boxes.append(vbox)

    return tuple(boxes)


# get the ssh config for a single box (id, name, provider, state, path)
def get_a_ssh_config(box):
    """Gives back a map of all the machine's ssh configurations"""

    try:
        output = subprocess.check_output(["vagrant", "ssh-config", box[1]], cwd=box[4])
    except subprocess.CalledProcessError:
        return
    except OSError:
        return

    config = SSHConfig()
    config.parse(StringIO(output))
    host_config = config.lookup(box[1])
    host_config['python_interpreter'] = "PATH=/home/core/bin:$PATH python"

    # man 5 ssh_config:
    # > It is possible to have multiple identity files ...
    # > all these identities will be tried in sequence.
    for id in host_config['identityfile']:
        if os.path.isfile(id):
            host_config['identityfile'] = id

    return {v: host_config[k] for k, v in _ssh_to_ansible}

# List out servers that vagrant has running
# ------------------------------
if options.list:
    ssh_config = get_ssh_config()
    meta = defaultdict(dict)
    hosts = []

    for host in ssh_config:
        if ssh_config[host] is not None:
            meta['hostvars'][host[1]] = ssh_config[host]
            hosts.append(host[1])

    print(json.dumps({_group: list(hosts), '_meta': meta}))
    sys.exit(0)

# Get out the host details
# ------------------------------
elif options.host:
    vbox = (options.host, options.host, "", "running", ".")
    for k in list_running_boxes():
        if options.host in k:
            vbox = k
    print(json.dumps(get_a_ssh_config(vbox)))
    sys.exit(0)

# Print out help
# ------------------------------
else:
    parser.print_help()
    sys.exit(0)
