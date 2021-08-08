#!/usr/bin/env bash

# use single quotes, escape single quotes, prefix every valid line with export
# partially extracted from here https://stackoverflow.com/questions/15783701/which-characters-need-to-be-escaped-when-using-bash
(cat ../../../../../../run/secrets/eva-cicd_env | sed -e '/^#/d;/^\s*$/d' -e "s/'/'\\\''/g" -e "s/=\(.*\)/='\1'/g" -e 's/^/export /') >triggers/gitbot/eva-cicd_env

DOCKER_BUILDKIT=1 docker build -t eva-cicd-gitbot-debian --target continuous-integration triggers/gitbot/

# clean env file
rm triggers/gitbot/eva-cicd_env
