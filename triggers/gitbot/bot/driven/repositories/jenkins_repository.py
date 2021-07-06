from abc import ABCMeta, abstractmethod


class JenkinsRepository(metaclass=ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'is_jenkins_running') and
                callable(subclass.is_jenkins_running) and
                hasattr(subclass, 'start_jenkins') and
                callable(subclass.start_jenkins) and
                hasattr(subclass, 'stop_jenkins') and
                callable(subclass.stop_jenkins) and
                hasattr(subclass, 'trigger_build') and
                callable(subclass.trigger_build) and
                hasattr(subclass, 'get_connection') and
                callable(subclass.get_connection) or
                NotImplemented)

    @abstractmethod
    def get_connection():
        raise NotImplementedError

    @abstractmethod
    def is_jenkins_running():
        raise NotImplementedError

    @abstractmethod
    def start_jenkins():
        raise NotImplementedError

    @abstractmethod
    def stop_jenkins():
        raise NotImplementedError

    @abstractmethod
    def trigger_build(job_name, parameters):
        raise NotImplementedError
