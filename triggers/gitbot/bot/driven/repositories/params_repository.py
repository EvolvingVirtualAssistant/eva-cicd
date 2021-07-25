from abc import ABCMeta, abstractmethod


class ParamsRepository(metaclass=ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_github_allowed_authors') and
                callable(subclass.get_github_allowed_authors) and
                hasattr(subclass, 'get_discord_token') and
                callable(subclass.get_discord_token) and
                hasattr(subclass, 'get_github_api_token') and
                callable(subclass.get_github_api_token) and
                hasattr(subclass, 'get_github_organization') and
                callable(subclass.get_github_organization) and
                hasattr(subclass, 'get_jenkins_url') and
                callable(subclass.get_jenkins_url) and
                hasattr(subclass, 'get_jenkins_username') and
                callable(subclass.get_jenkins_username) and
                hasattr(subclass, 'get_jenkins_password') and
                callable(subclass.get_jenkins_password) and
                hasattr(subclass, 'get_jenkins_connection_timeout') and
                callable(subclass.get_jenkins_connection_timeout) and
                hasattr(subclass, 'get_jenkins_ready_timeout') and
                callable(subclass.get_jenkins_ready_timeout) and
                hasattr(subclass, 'get_jenkins_all_nodes_online_timeout') and
                callable(subclass.get_jenkins_all_nodes_online_timeout) and
                hasattr(subclass, 'get_jenkins_shutdown_timeout') and
                callable(subclass.get_jenkins_shutdown_timeout) or
                NotImplemented)

    @abstractmethod
    def get_discord_token():
        raise NotImplementedError

    @abstractmethod
    def get_github_allowed_authors():
        raise NotImplementedError

    @abstractmethod
    def get_github_api_token():
        raise NotImplementedError

    @abstractmethod
    def get_github_organization():
        raise NotImplementedError

    @abstractmethod
    def get_jenkins_url():
        raise NotImplementedError

    @abstractmethod
    def get_jenkins_username():
        raise NotImplementedError

    @abstractmethod
    def get_jenkins_password():
        raise NotImplementedError

    @abstractmethod
    def get_jenkins_connection_timeout():
        raise NotImplementedError

    @abstractmethod
    def get_jenkins_ready_timeout():
        raise NotImplementedError

    @abstractmethod
    def get_jenkins_all_nodes_online_timeout():
        raise NotImplementedError

    @abstractmethod
    def get_jenkins_shutdown_timeout():
        raise NotImplementedError
