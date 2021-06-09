FROM jenkins/ssh-agent:latest-jdk11

# copy entrypoint script
COPY jenkins-agent-entrypoint.sh /usr/local/bin/jenkins-agent-entrypoint.sh
RUN chmod 755 /usr/local/bin/jenkins-agent-entrypoint.sh

# create shared group between root and jenkins users 
# giving root folder ownership to that group
ARG SHARED_GROUP=rootjenkinsshared
RUN groupadd -g 1001 ${SHARED_GROUP} && \
    usermod -aG ${SHARED_GROUP} jenkins && \
    usermod -aG ${SHARED_GROUP} root && \
    chown -hR root:${SHARED_GROUP} /root && \
    chmod 770 /root

ENTRYPOINT ["jenkins-agent-entrypoint.sh"]