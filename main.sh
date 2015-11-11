#!/bin/sh
export EC2_INI_PATH=inventory/ec2.ini
unset ANSIBLE_SSH_ARGS

# read input parameters
vflag=""
prov="ec2"
gaia_fleet_dir=".gaia-fleet"

while [ $# -gt 0 ]
do
  case "$1" in
    -v) vflag="-vvvv";;
    -f) yamlfile="$2"; shift;;
    -e) environ="$2"; shift;;
    -p) prov="$2"; shift;;
    -g) gaia_fleet_dir="$2"; shift;;
    -e) env="$2"; shift;;
    -s) service="$2"; shift;;
    -p) provisioner="$2"; shift;;
    -h)
        echo >&2 "usage: $0 -e environment [-p provisioner: default 'ec2'] -f yamlfile [-s service] [-v]"
        exit 1;;
     *) break;; # terminate while loop
  esac
  shift
done

# ignore SSH arguments defined in <ansible.cfg> file: tunneling through Bastion VM to CoreOS cluster
if [ "${prov}" = "vagrant" ]
then
  export ANSIBLE_SSH_ARGS=""
fi

ansible-playbook --extra-vars "environ=${environ} service=${service} provisioner=${prov} gaia_fleet_dir=${gaia_fleet_dir}" ${yamlfile} ${vflag}
