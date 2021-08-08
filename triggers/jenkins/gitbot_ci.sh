#!/usr/bin/env bash

whoami
#chown jenkins ../../../../../../run/secrets/eva-cicd_env Read-only file system
cat ../../../../../../run/secrets/eva-cicd_env >triggers/gitbot/eva-cicd_env
cat triggers/gitbot/eva-cicd_env

# find and read the appropriate file that was copied to the agent container
# set all of the read env vars only in the context of this file
# add in the line below dynamically --env VAR_NAME, which will copy the env and pass it to the container
DOCKER_BUILDKIT=1 docker build -t eva-cicd-gitbot-debian --target continuous-integration triggers/gitbot/

# clean env file
rm triggers/gitbot/eva-cicd_env
#grep -v '^#' triggers/gitbot/eva-cicd_env | xargs -d '\n'

#source <(sed -E -n 's/[^#]+/export &/ p' triggers/gitbot/eva-cicd_env)
