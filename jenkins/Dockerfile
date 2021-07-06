# --------------------------------------
# packaging jenkins plugins
FROM maven:3.8.1-openjdk-8-slim as build-plugins  
RUN mkdir -p /usr/src/app
COPY plugins/pipeline-as-yaml-workflow-multi-branch-plugin/pom.xml /usr/src/app
RUN mvn -f /usr/src/app/pom.xml clean -B dependency:resolve dependency:resolve-plugins
COPY plugins/pipeline-as-yaml-workflow-multi-branch-plugin/src /usr/src/app/src
RUN mvn -f /usr/src/app/pom.xml package -DskipTests

# --------------------------------------

FROM jenkins/jenkins:lts-jdk11
USER root
RUN apt-get update && apt-get install -y apt-transport-https \
    ca-certificates curl gnupg2 \
    software-properties-common
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
RUN apt-key fingerprint 0EBFCD88
RUN add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/debian \
    $(lsb_release -cs) stable"
RUN apt-get update && apt-get install -y docker-ce-cli

USER jenkins
RUN jenkins-plugin-cli --plugins "blueocean:1.24.7 docker-workflow:1.26 git:4.7.2 pipeline-as-yaml:0.16-rc locale:1.4 ssh-slaves:1.31.7 ssh-credentials:1.19 git:4.7.2 configuration-as-code:1.51 job-dsl:1.77"

USER root

ARG JENKINS_EVA_PLUGINS=/home/eva_plugins
RUN mkdir ${JENKINS_EVA_PLUGINS}
COPY --from=build-plugins /usr/src/app/target/pipeline-as-yaml-workflow-multi-branch-plugin.hpi ${JENKINS_EVA_PLUGINS}/pipeline-as-yaml-workflow-multi-branch-plugin.hpi

RUN apt-get update && apt-get install -y gawk

# create shared group between root and jenkins users 
# giving root folder ownership to that group
ARG SHARED_GROUP=rootjenkinsshared
RUN groupadd -g 1001 ${SHARED_GROUP} && \
    usermod -aG ${SHARED_GROUP} jenkins && \
    usermod -aG ${SHARED_GROUP} root && \
    chown -hR root:${SHARED_GROUP} /root && \
    chmod 770 /root

ARG JENKINS_EVA_SCRIPTS=/home/eva_scripts
RUN mkdir ${JENKINS_EVA_SCRIPTS} && \
    mkdir ${JENKINS_EVA_SCRIPTS}/casc_configs

# copy jenkins.yaml file used by configuration as code plugin
COPY jenkins.yaml ${JENKINS_EVA_SCRIPTS}/casc_configs/jenkins.yaml

# copy jenkins groovy scripts
COPY scripts/ ${JENKINS_EVA_SCRIPTS}
COPY setup-initial-configs-jenkins.sh ${JENKINS_EVA_SCRIPTS}/setup-initial-configs-jenkins.sh

RUN chown -hR jenkins:jenkins ${JENKINS_EVA_SCRIPTS} && \
    chmod -R 755 ${JENKINS_EVA_SCRIPTS} && \
    chown -hR jenkins:jenkins ${JENKINS_EVA_PLUGINS} && \
    chmod -R 755 ${JENKINS_EVA_PLUGINS}

# copy entrypoint script
COPY jenkins-entrypoint.sh /usr/local/bin/jenkins-entrypoint.sh
RUN chmod 755 /usr/local/bin/jenkins-entrypoint.sh

USER jenkins

ENTRYPOINT ["/sbin/tini", "--", "jenkins-entrypoint.sh"]
