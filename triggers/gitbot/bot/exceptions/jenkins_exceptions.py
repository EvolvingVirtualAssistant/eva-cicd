class JenkinsError(Exception):
    """Basic exception for error related to jenkins"""

    def __init__(self, msg=None):
        if msg is None:
            msg = "Error while using jenkins"
        super().__init__(msg)


class JenkinsNoConnectionError(JenkinsError):
    """Exception when there is no connection established with jenkins"""

    def __init__(self, msg=None):
        if msg is None:
            msg = "There is no connection established with jenkins"
        super().__init__(msg)


class JenkinsStartingError(JenkinsError):
    """Exception when there is an error starting jenkins"""

    def __init__(self, stderr=None, msg=None):

        if msg is None:
            msg = "There was an error starting jenkins"

        if stderr is not None:
            msg += " -> {}".format(stderr)

        super().__init__(msg)


class JenkinsStoppingError(JenkinsError):
    """Exception when there is an error stopping jenkins"""

    def __init__(self, stderr=None, msg=None):

        if msg is None:
            msg = "There was an error stopping jenkins"

        if stderr is not None:
            msg += " -> {}".format(stderr)

        super().__init__(msg)
