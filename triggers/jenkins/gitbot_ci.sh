#!/usr/bin/env bash

DOCKER_BUILDKIT=1 docker build -t eva-cicd-gitbot-debian --target continuous-integration gitbot/
