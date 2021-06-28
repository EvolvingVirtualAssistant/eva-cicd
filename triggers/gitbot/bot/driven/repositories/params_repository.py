from abc import ABCMeta, abstractmethod


class ParamsRepository(metaclass=ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_github_allowed_authors') and
                callable(subclass.get_github_allowed_authors) and
                hasattr(subclass, 'get_discord_token') and
                callable(subclass.get_discord_token) and
                hasattr(subclass, 'get_github_token') and
                callable(subclass.get_github_token) or
                NotImplemented)

    @abstractmethod
    def get_discord_token():
        raise NotImplementedError

    @abstractmethod
    def get_github_allowed_authors():
        raise NotImplementedError

    @abstractmethod
    def get_github_token():
        raise NotImplementedError
