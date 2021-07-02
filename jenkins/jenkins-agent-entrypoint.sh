#!/usr/bin/env bash

#KEY=$(cat /home/jenkins_shared_secrets/jenkins_eva_agent1_key.pub)
KEY=$(cat /run/secrets/jenkins_eva_agent1_pub_key)

VARS1="HOME=|USER=|MAIL=|LC_ALL=|LS_COLORS=|LANG="
VARS2="HOSTNAME=|PWD=|TERM=|SHLVL=|LANGUAGE=|_="
VARS="${VARS1}|${VARS2}"
env | egrep -v '^(${VARS})' >>/etc/environment

command /usr/local/bin/setup-sshd "$KEY"
