## Requirements to run jenkins
### Secrets:
- Create a github organization and app. Guides: https://www.youtube.com/watch?v=LbXKUKQ24T8 ; https://docs.cloudbees.com/docs/cloudbees-ci/latest/cloud-admin-guide/github-app-auth
- **github-app-id-jenkins-eva.txt** file that contains the github app id
- **converted-github-app-jenkins-eva.pem** file should contain the ssh private key used to interact with the github app created on the E.V.A organization repository. The key in this file has been converted using 
  ```sh
  openssl pkcs8 -topk8 -inform PEM -outform PEM -in github-app-generated-private-key.pem -out converted-github-app-jenkins-eva.pem -nocrypt
  ``` 
  in order for jenkins to be able to use the private key
- **jenkins_admin_password.txt** file should contain the new jenkins admin password  
- **jenkins_eva_agent1_key** and **jenkins_eva_agent1_key.pub** files will be the public private key pair used to establish an ssh connection between the jenkins container and jenkins agent 1 container. One can generate the key pair with the following command:
  ```sh
  # assuming that you are running this command from jenkins folder inside of eva-cicd repository 
  ssh-keygen -f .secrets/jenkins_eva_agent1_key -N password_for_the_key
  ``` 
All of these secrets will then have to be injected into the docker containers. There are multiple ways of achieving that, for now we are using the *docker-compose.yml* file to have all of these secrets defined there.

## Running gitbot
One should run gitbot since gitbot will also start jenkins based on PRs notifications that git hook picks up.
### Start
```sh
cd triggers/gitbot
python -m bot # Run bot module which start a gitbot in discord
```  
## Running jenkins

### Build
```sh
cd jenkins
docker-compose build
``` 
### Start
```sh
cd jenkins
docker-compose up -d # Run containers in the background
```   
### Stop
```sh
cd jenkins
docker-compose stop
```