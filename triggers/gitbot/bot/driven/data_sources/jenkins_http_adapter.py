from bot.exceptions import JenkinsNoConnectionError
from bot.driven.repositories import JenkinsRepository, ParamsRepository
import jenkins
import logging


logger = logging.getLogger(__name__)


class JenkinsHttpAdapter(JenkinsRepository):
    def __init__(self, paramsRespository: ParamsRepository):
        self.paramsRespository = paramsRespository
        self.server = None

    def get_connection(self) -> jenkins.Jenkins:
        if self.server is None:
            try:
                self.server = jenkins.Jenkins(
                    self.paramsRespository.get_jenkins_url(),
                    username=self.paramsRespository.get_jenkins_username(),
                    password=self.paramsRespository.get_jenkins_password(),
                    timeout=self.paramsRespository.get_jenkins_connection_timeout())

                if not self.server.wait_for_normal_op(self.paramsRespository.get_jenkins_ready_timeout()):
                    self.server = None
                    logger.error("Jenkins is not ready")

            except Exception as ex:
                self.server = None
                logger.exception("Error establishing connection to jenkins")
        return self.server

    def is_jenkins_running(self):
        self.server = self.get_connection()

        if self.server is None:
            return False

        return True

    def start_jenkins(self):
        if self.is_jenkins_running():
            return

        pass
        # call docker-compose

    def stop_jenkins(self):
        try:
            self.server.quiet_down()
        except Exception as ex:
            logger.exception("Error while quietting down jenkins")

        pass
        # call command to stop docker

    def trigger_build(self, job_name="", parameters=None):
        if self.server is None:
            raise JenkinsNoConnectionError

        next_build_number = self.server.get_job_info(job_name)[
            'nextBuildNumber']
        # ["lastCompleteBuild"]["number"]
        output = self.server.build_job(job_name, parameters)

        build_info = self.server.get_build_info(job_name, next_build_number)
