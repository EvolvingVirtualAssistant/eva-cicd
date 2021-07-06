#!/usr/bin/env bash

username=${JENKINS_USERNAME}
old_password=$(cat /var/jenkins_home/secrets/initialAdminPassword)
new_password=$(cat /run/secrets/jenkins_admin_password)

http_status=''
response=''
cookie_session_id=''
crumb=''

function log() {
    echo "[$(date "+%Y-%m-%d %H:%M:%S")][setup-script] $1"
}

function GET_request() {
    response="$(curl -s -k -i -X GET --header 'Content-type: application/json' --user "$1":"$2" "$3")"
}

function get_http_status() {
    http_status=$(echo "$1" | grep HTTP | awk '{print $2}')
}

function get_cookie_session_id() {
    cookie_session_id=$(echo "$1" | grep "Set-Cookie" | awk '{print $2}')
    cookie_session_id="${cookie_session_id%\;}"
}

function get_jenkins_crumb() {
    crumb=$(echo "$1" | grep 'crumb' | awk 'BEGIN { FS = "," } ; {print $2 }' | awk 'BEGIN { FS = ":" } ; { print $2 }')
    crumb="${crumb%\"}"
    crumb="${crumb#\"}"
}

function GET_jenkins_crumb() {
    GET_request "$1" "$2" 'http://localhost:8080/crumbIssuer/api/json'
}

function POST_create_jenkins_api_token() {
    response="$(curl -s http://localhost:8080/user/$username/descriptorByName/jenkins.security.ApiTokenProperty/generateNewToken --data "newTokenName=initConfigToken " --user "$1":"$2" -H "Jenkins-Crumb: $3 " -H "Cookie: $4")"
}

function get_jenkins_api_token() {
    api_token=$(echo "$1" | grep 'tokenValue' | awk 'BEGIN { FS = "," } ; {print $4 }' | awk 'BEGIN { FS = ":" } ; { print $2 }')
    api_token="${api_token%\}}"
    api_token="${api_token%\}}"
    api_token="${api_token%\"}"
    api_token="${api_token#\"}"
}

function execute_script_in_jenkins() {
    response="$(curl -s --user "$1:$2" --data-urlencode "script=$(<"$3")" http://localhost:8080/scriptText)"
    log "$response"
}

function download_jenkins_cli() {
    response="$(curl -s http://localhost:8080/jnlpJars/jenkins-cli.jar --output "${JENKINS_EVA_PLUGINS}"/jenkins-cli.jar)"
    log "$response"
}

function check_if_jenkins_user_already_has_password_set() {
    local isUnauthorized
    isUnauthorized="$(echo "$http_status" | grep 401)"
    if [ -n "$isUnauthorized" ]; then
        log "Wrong password. Authenticating with new password."
        GET_jenkins_crumb "$username" "$new_password"
        get_http_status "$response"
        local isAuthorized
        isAuthorized="$(echo "$http_status" | grep 200)"
        if [ -n "$isAuthorized" ]; then
            log "Jenkins user already has the right credentials"
            old_password=$new_password
        fi
    fi
}

function wait_for_jenkins_start() {
    local nRetries=0
    local nMaxRetries=50
    # checks to see if jenkins is up and ready to use
    while [ "$http_status" != 200 ] && [ $nRetries -lt $nMaxRetries ]; do
        sleep 10
        GET_jenkins_crumb "$username" "$old_password"
        get_http_status "$response"
        log "Jenkins responded with status: $http_status"
        nRetries=$((nRetries + 1))

        check_if_jenkins_user_already_has_password_set
    done
}

function create_new_api_token() {
    get_cookie_session_id "$response"
    if [ -z "$cookie_session_id" ] || [ "$cookie_session_id" == " " ]; then
        log "Could not extract cookie session id from $response. Terminating."
        exit 1
    fi

    get_jenkins_crumb "$response"
    if [ -z "$crumb" ] || [ "$crumb" == " " ]; then
        log "Could not extract crumb from $response. Terminating."
        exit 1
    fi

    POST_create_jenkins_api_token "$username" "$new_password" "$crumb" "$cookie_session_id"
    get_jenkins_api_token "$response"
    if [ -z "$api_token" ] || [ "$api_token" == " " ]; then
        log "Could not extract api token from $response. Terminating."
        exit 1
    fi
}

log "Starting initial jenkins config setup..."

wait_for_jenkins_start

create_new_api_token

# Uploads plugins
download_jenkins_cli
java -jar "${JENKINS_EVA_PLUGINS}"/jenkins-cli.jar -s http://localhost:8080 -auth "$username":"$api_token" install-plugin "file:///${JENKINS_EVA_PLUGINS}/pipeline-as-yaml-workflow-multi-branch-plugin.hpi" -restart

log "Sleeping for 20 seconds waiting restart..."
sleep 20

http_status=''
response=''
cookie_session_id=''
crumb=''

wait_for_jenkins_start

create_new_api_token

log "Restarting jenkins config setup..."

# Change user password if user still uses the default generated password
if [ "$old_password" != "$new_password" ]; then
    log "Trying to change jenkins user password..."
    execute_script_in_jenkins "$username" "$api_token" "${JENKINS_EVA_SCRIPTS}/change-password.groovy"
else
    log "Skipping password change step"
fi

# Set locale options
log "Trying to set locale options..."
execute_script_in_jenkins "$username" "$api_token" "${JENKINS_EVA_SCRIPTS}/set-locale-options.groovy"

# Add jenkins agent ssh credential - no longer needed since ssh key is already defined in jenkins.yaml configuration
#execute_script_in_jenkins "$username" "$api_token" "${JENKINS_EVA_SCRIPTS}/add-agent-ssh-credentials.groovy"

# Add jenkins agent
log "Trying to add jenkins agent..."
execute_script_in_jenkins "$username" "$api_token" "${JENKINS_EVA_SCRIPTS}/add-permanent-agent.groovy"

log "Jenkins successfully configured"
