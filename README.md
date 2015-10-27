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

Deployment playbooks require keys/ssh_config file to be generated. This file is generated by ssh_config_amazon.yaml from ansible-coreos-cluster for connecting from localhost to amazon. This file needs to be regenerated in case some new machines were started in amazon auto-scale group.

```
ansible-playbook ssh_config_amazon.yaml
```

The generated file cannot be moved to other location, otherwise path to the file ssh_config must be adjusted in it. This path is required by ProxyCommand option which doesn't consider owner process command line arguments.

User may use the generated ssh_config to connect to any EC2 Gaia machine without having to use ssh-agent/ssh-add:
```
ssh -F keys/ssh_config serverIp
```

For the list of IPs see ssh_config.

# Deployment playbooks

All deployment playbooks assume "gaia-fleet" directory is available from parent directory.

There are several playbooks for management of services:
- deploy_all.yaml - (re)deploys all services
- deploy_core_services.yaml - (re)deploys services considered core - i.e skyDNS, registrator, rabbitmq, influxdb
- deploy_gaia_services.yaml - (re)deploys main gaia services
- deploy_service.yaml - (re)deploys single service selected by --extra-vars="service=someServicePrefix". For example running it with --extra-vars="service=sky" will redeploy skyDNS
- stop_all.yaml - stops all services
- stop_gaia_services.yaml - stops main gaia services
- start_all.yaml - starts all services
- start_gaia_services.yaml - starts main gaia services
- destroy_all.yaml - destroys all services
- destroy_gaia_services.yaml - destroys main gaia services

Examples:

to (re)deploy everything run:
```
ansible-playbook deploy_all.yaml
```

to (re)deploy haproxy run:
```
ansible-playbook deploy_service.yaml --extra-vars="service=haproxy"
```
