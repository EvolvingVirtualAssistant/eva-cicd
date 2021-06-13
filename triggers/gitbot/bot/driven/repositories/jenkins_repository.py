from abc import ABCMeta, abstractmethod


class JenkinsRepository(metaclass=ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'check_jenkins_is_up') and
                callable(subclass.check_jenkins_is_up) and
                hasattr(subclass, 'start_jenkins') and
                callable(subclass.start_jenkins) and
                hasattr(subclass, 'stop_jenkins') and
                callable(subclass.stop_jenkins) and
                hasattr(subclass, 'send_message_to_jenkins') and
                callable(subclass.send_message_to_jenkins) or
                NotImplemented)

    @abstractmethod
    def check_jenkins_is_up():
        raise NotImplementedError

    @abstractmethod
    def start_jenkins():
        raise NotImplementedError

    @abstractmethod
    def stop_jenkins():
        raise NotImplementedError

    @abstractmethod
    def send_message_to_jenkins():
        raise NotImplementedError
