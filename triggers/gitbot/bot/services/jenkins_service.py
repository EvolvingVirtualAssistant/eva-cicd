from driven.repositories import JenkinsRepository


class JenkinsService():

    def __init__(self, jenkinsRepository: JenkinsRepository):
        self.jenkinsRepository = jenkinsRepository

    def check_jenkins():
        pass
        # check if jenkins is running

    def start_jenkins():
        pass
        # start jenkins if it is not running

    def send_message_to_jenkins(self, prUrl: str):
        pass
