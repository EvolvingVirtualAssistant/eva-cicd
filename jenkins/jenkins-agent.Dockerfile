FROM jenkins/ssh-agent:latest-jdk11

# create shared group between root and jenkins users 
# giving root folder ownership to that group
ARG SHARED_GROUP=rootjenkinsshared
RUN groupadd -g 1001 ${SHARED_GROUP} && \
    usermod -aG ${SHARED_GROUP} jenkins && \
    usermod -aG ${SHARED_GROUP} root && \
    chown -hR root:${SHARED_GROUP} /root && \
    chmod 770 /root

# installs docker
RUN apt-get update && apt-get install -y apt-transport-https \
    ca-certificates curl gnupg2 \
    software-properties-common
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
RUN apt-key fingerprint 0EBFCD88
RUN add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/debian \
    $(lsb_release -cs) stable"
RUN apt-get update && apt-get install -y docker-ce docker-ce-cli containerd.io

# adds root to group docker and update iptables to use the legacy alternatives (needed to run docker inside docker) 
RUN usermod -aG docker root \
    && usermod -aG docker jenkins \
    && update-alternatives --set iptables /usr/sbin/iptables-legacy \
    && update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy \
    && systemctl enable docker.service \
    && systemctl enable containerd.service

# copy secrets from other eva repositories
RUN mkdir -p /home/eva/.secrets/
COPY .secrets/eva-investments /home/eva/.secrets/eva-investments

# copy entrypoint script
COPY jenkins-agent-entrypoint.sh /usr/local/bin/jenkins-agent-entrypoint.sh
RUN chmod 755 /usr/local/bin/jenkins-agent-entrypoint.sh

ENTRYPOINT ["jenkins-agent-entrypoint.sh"]