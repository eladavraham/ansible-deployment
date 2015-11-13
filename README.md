# ansible-deployment
Ansible playbooks for EC2 Gaia deployment

These playbooks assumes ansible-bastion and ansible-coreos-cluster have been executed and cluster is ready for service deployment. This means all coreos instances must be ready for SSH connections.

# setup environment

In order to run these playbooks you need to have the following installed on your machine:
- Python 2.7.x
- pip - Python package manager
- pip modules:
  - ansible - Ansible tool
  - awscli - Amazon CLI for Python
  - boto - AWS libraries

Run following command to install required modules
```
pip install ansible awscli boto
```

You will need also to setup the following ENV variables:
```
export AWS_ACCESS_KEY_ID=A...XXX
export AWS_SECRET_ACCESS_KEY=5....XXXX
export AWS_DEFAULT_REGION='us-west-2'
export AWS_DEFAULT_AZ1='us-west-2a'
export AWS_DEFAULT_AZ2='us-west-2b'
export AWS_DEFAULT_AZ3='us-west-2c'
export AWS_DEFAULT_AZ4='us-west-2a'

```
> **Note**: protect your AWS access key and secret access key

AWS credentials can also be stored in $HOME/.aws/credentials file.

`ec2.py` script is used to setup Ansible [Dynamic Inventory](http://docs.ansible.com/ansible/intro_dynamic_inventory.html) for AWS EC2.

# SSH configuration

Deployment playbooks require keys/ssh_config file to be generated. **ssh_config** file generation can be done by running `ssh_config_amazon.yaml` playbook from [ansible-coreos-cluster](https://github.com/gaia-adm/ansible-coreos-cluster) repository. 

User may use the generated ssh_config to connect to any EC2 Gaia machine without having to use ssh-agent/ssh-add:
```
ssh -F keys/ssh_config serverIp
```

For the list of IPs see ssh_config.

# Deployment to Vagrant CoreOS cluster

It's possbile to deploy Gaia services to CoreOS cluster running inside Vagrant. 
In order to do this, you need to use `vagrant.py` dynamic inventory script and set `provisioner` environment variable to `vagrant`.

You will also need to skip **ssh_args** from **ansible.cfg** file. This can be done by resetting ANSIBLE_SSH_ARGS ENV variable.

For example:
```
export ANSIBLE_SSH_ARGS=""
ansible-playbook -i inventory/vagrant.py -e "provisioner=vagrant" deploy_all.yaml
```

# Deployment playbooks

All service files will be automatically downloaded into `.gaia-fleet` folder (customizable through environment variable). By default fleet service files will be downloaded from `master` branch, but it's possible to customize branch per service file.


There are several playbooks for management of services:
- deploy_all.yaml - (re)deploys all services
- deploy_system_services.yaml - (re)deploys services considered system - i.e skyDNS, registrator
- deploy_platform_services.yaml - (re)deploys services considered platform - i.e rabbitmq, influxdb
- deploy_gaia_services.yaml - (re)deploys main gaia services
- deploy_service.yaml - (re)deploys single service selected by --extra-vars="service=someServicePrefix". For example running it with --extra-vars="service=sky" will redeploy skyDNS
- stop_all.yaml - stops all services
- stop_gaia_services.yaml - stops main gaia services
- start_all.yaml - starts all services
- start_gaia_services.yaml - starts main gaia services
- destroy_all.yaml - destroys all services
- destroy_gaia_services.yaml - destroys main gaia services

There is main.sh script that helps invoke all of the yamls, to print usage type:
```
./main.sh -h
```

Examples:

to (re)deploy everything run:
```
./main.sh -e production -f deploy_all.yaml
```

to (re)deploy haproxy run:
```
./main.sh -e production -f deploy_service.yaml -s haproxy
```

# Monitoring

For OS level monitoring, Amazon Cloud Watch is used and per machine metrics are visible in Amazon EC2 console.

For Docker level monitoring cAdvisor is used on each coreos node, accessible through port 8050. CAdvisor can be accessed from local machine via SSH tunneling:

```
ssh -L yourlocalIP:8050:coreosIP:8050 -F keys/ssh_config bastionHostname
```

In Linux there is no need to specify 'yourlocalIP'. In Windows / vagrant environment 'yourlocalIP' needs to be an IP address on VM reachable from the Windows host.

Point your browser to http://yourlocalIP:8050 to see cAdvisor. If proxy is used you may have to add an exception. At this point there is no centralized service where cAdvisor data can be accessed for the whole coreos cluster.
