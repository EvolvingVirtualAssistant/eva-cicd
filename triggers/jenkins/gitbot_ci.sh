#!/usr/bin/env bash

(cat ../../../../../../run/secrets/eva-cicd_env | sed -e '/^#/d;/^\s*$/d' -e "s/'/'\\\''/g" -e "s/=\(.*\)/='\1'/g" -e 's/^/export /') >triggers/gitbot/eva-cicd_env
cat triggers/gitbot/eva-cicd_env

# find and read the appropriate file that was copied to the agent container
# set all of the read env vars only in the context of this file
# add in the line below dynamically --env VAR_NAME, which will copy the env and pass it to the container
DOCKER_BUILDKIT=1 docker build -t eva-cicd-gitbot-debian --target continuous-integration triggers/gitbot/

# clean env file
rm triggers/gitbot/eva-cicd_env
