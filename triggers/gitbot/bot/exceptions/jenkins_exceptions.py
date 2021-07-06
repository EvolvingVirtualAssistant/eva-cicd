class JenkinsError(Exception):
    """Basic exception for error related to jenkins"""

    def __init__(self, msg=None):
        if msg is None:
            msg = "Error while communicating with jenkins"
        super(JenkinsError, self).__init__(msg)


class JenkinsNoConnectionError(JenkinsError):
    """Exception when there is no connection established with jenkins"""

    def __init__(self, msg=None):
        if msg is None:
            msg = "There is no connection established with jenkins"
        super(JenkinsNoConnectionError, self).__init__(msg)
