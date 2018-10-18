#!/usr/bin/env bash

set -x # echo commands
set -e # fast fail
export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get -y upgrade
apt-get -y install curl
apt-get -y install git

# docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
apt-get update
apt-cache policy docker-ce
apt-get -y install docker-ce
service docker restart
