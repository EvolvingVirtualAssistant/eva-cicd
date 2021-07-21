#!/usr/bin/env bash

function log() {
    echo "[$(date "+%Y-%m-%d %H:%M:%S")][jenkins-agent-entrypoint] $1"
}

KEY=$(cat /run/secrets/jenkins_eva_agent1_pub_key)

VARS1="HOME=|USER=|MAIL=|LC_ALL=|LS_COLORS=|LANG="
VARS2="HOSTNAME=|PWD=|TERM=|SHLVL=|LANGUAGE=|_="
VARS="${VARS1}|${VARS2}"
env | egrep -v '^(${VARS})' >>/etc/environment

log "Start docker service..."
service docker start
service docker status

function wait_for_docker_sock_file() {
    local docker_file=/var/run/docker.sock
    local nRetries=0
    local nMaxRetries=20
    while [ ! -e "$docker_file" ] && [ $nRetries -lt $nMaxRetries ]; do
        log "File $docker_file not found. Sleeping for 10 seconds"
        sleep 10
        nRetries=$((nRetries + 1))
    done
}

log "Waiting for docker.sock file creation"
wait_for_docker_sock_file

log "Changing permissions of docker.sock file"
chmod 666 /var/run/docker.sock

command /usr/local/bin/setup-sshd "$KEY"
