#!/bin/sh
export EC2_INI_PATH=inventory/ec2.ini

# read input parameters
vflag=""
provisioner="ec2"
gaia_fleet_dir=".gaia-fleet"
while [ $# -gt 0 ]
do
  case "$1" in
    -v) vflag="-vvvv";;
    -f) yamlfile="$2"; shift;;
    -g) gaia_fleet_dir="$2"; shift;;
    -e) env="$2"; shift;;
    -s) service="$2"; shift;;
    -p) provisioner="$2"; shift;;
    -h)
        echo >&2 "usage: $0 -e environment -f yamlfile <-s service> -v"
        exit 1;;
     *) break;; # terminate while loop
  esac
  shift
done

ansible-playbook --extra-vars "env=$env provisioner=$provisioner gaia_fleet_dir=$gaia_fleet_dir service=$service" $yamlfile $vflag
