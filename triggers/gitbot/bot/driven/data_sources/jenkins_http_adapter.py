from driven.repositories import JenkinsRepository


class JenkinsHttpAdapter(JenkinsRepository):
    def __init__(self):
        pass

    def check_jenkins_is_up():
        raise NotImplementedError

    def start_jenkins():
        raise NotImplementedError

    def stop_jenkins():
        raise NotImplementedError

    def send_message_to_jenkins():
        raise NotImplementedError
