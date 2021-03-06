import logging
from os.path import join, dirname, abspath
import subprocess
import threading
import time
import jenkins
from bot.exceptions import JenkinsNoConnectionError, JenkinsStartingError, JenkinsStoppingError
from bot.driven.repositories import JenkinsRepository, ParamsRepository


logger = logging.getLogger(__name__).parent


class JenkinsHttpAdapter(JenkinsRepository):

    WAITING_EXECUTOR_KEYWORD = 'why'
    RUNNING_EXECUTOR_KEYWORD = 'executable'
    NODE_OFFLINE_PROPERTY = 'offline'
    JOB_SUCCESS = 'SUCCESS'

    def __init__(self, params_repository: ParamsRepository):
        self.params_repository = params_repository
        self.server = None

    def _all_nodes_online(self, timeout):
        nodes_online = False
        start_time = time.time()
        while not nodes_online:
            try:
                nodes = self.server.get_nodes()
                nodes_online = True
                for node in nodes:
                    if node.get(JenkinsHttpAdapter.NODE_OFFLINE_PROPERTY, True):
                        nodes_online = False
            except Exception:
                pass

            if not nodes_online and time.time() > start_time + timeout:
                return False

        return True

    def _connect(self):
        if self.is_jenkins_running():
            return

        try:
            self.server = jenkins.Jenkins(
                self.params_repository.get_jenkins_url(),
                username=self.params_repository.get_jenkins_username(),
                password=self.params_repository.get_jenkins_password(),
                timeout=self.params_repository.get_jenkins_connection_timeout())

            nodes_timeout = self.params_repository.get_jenkins_all_nodes_online_timeout()
            ready_timeout = self.params_repository.get_jenkins_ready_timeout()

            if not self._all_nodes_online(nodes_timeout) or \
                    not self.server.wait_for_normal_op(ready_timeout):
                self.server = None
                logger.error("Jenkins is not ready")

        except Exception as ex:
            self.server = None
            logger.exception(
                "Error establishing connection to jenkins: {}".format(ex))

    # pylint: disable=no-self-use
    def _get_jenkins_docker_compose_path(self):
        return abspath(join(dirname(__file__), '../../../../../jenkins/docker-compose.yml'))

    def _wait_for_build(self, job_name, queue_item_number, next_build_number, on_complete):
        build_started = False

        while not build_started:
            item_info: dict = self.server.get_queue_item(queue_item_number)
            if item_info.get(JenkinsHttpAdapter.WAITING_EXECUTOR_KEYWORD) is None and \
                    item_info.get(JenkinsHttpAdapter.RUNNING_EXECUTOR_KEYWORD) is not None:
                build_started = True
            else:
                time.sleep(1)

        build_running = True
        build_info = None
        while build_running:
            build_info = self.server.get_build_info(
                job_name, next_build_number)
            if build_info.get('result') is not None:
                build_running = False
            else:
                time.sleep(1)

        url = build_info.get('url')
        result = build_info.get('result')
        logger.info(
            "build for url={} completed with result={}".format(url, result))
        on_complete("result={}\nurl={}".format(result, url), url,
                    result == JenkinsHttpAdapter.JOB_SUCCESS)

    def _clean_jenkins_server_crumb(self):
        # Setting crumb to None forces a new crumb to be obtained in the build_job request,
        # instead of using the previously created one, which seems to solve the error:
        # "HTTP ERROR 403 No valid crumb was included in the request"
        self.server.crumb = None

    def is_jenkins_running(self):
        if self.server is None:
            return False

        nodes_timeout = self.params_repository.get_jenkins_all_nodes_online_timeout()
        ready_timeout = self.params_repository.get_jenkins_ready_timeout()

        return self._all_nodes_online(nodes_timeout) and \
            self.server.wait_for_normal_op(ready_timeout)

    def start_jenkins(self):
        if self.is_jenkins_running():
            return

        run_args = ['docker-compose', '-f',
                    self._get_jenkins_docker_compose_path(), 'up', '-d']
        docker_compose = subprocess.run(run_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        universal_newlines=True, check=True)

        try:
            docker_compose.check_returncode()
            self._connect()
            logger.info("Jenkins started")
        except subprocess.CalledProcessError as ex:
            logger.exception(
                "Error while starting jenkins, through docker-compose command: {}"
                .format(docker_compose.stderr))
            raise JenkinsStartingError(stderr=docker_compose.stderr) from ex

    def stop_jenkins(self):
        if not self.is_jenkins_running():
            return

        try:
            self._clean_jenkins_server_crumb()
            self.server.quiet_down()
        except Exception:
            logger.exception("Error while quietting down jenkins")

        run_args = ['docker-compose', '-f',
                    self._get_jenkins_docker_compose_path(), 'stop']
        docker_compose = subprocess.run(run_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        universal_newlines=True, check=True)

        try:
            docker_compose.check_returncode()
            self.server = None
            logger.info("Jenkins stopped")
        except subprocess.CalledProcessError as ex:
            logger.exception(
                "Error while stopping jenkins, through docker-compose command: {}"
                .format(docker_compose.stderr))
            raise JenkinsStoppingError(stderr=docker_compose.stderr) from ex

    def trigger_build(self, on_complete, job_name="", parameters=None):
        if not self.is_jenkins_running():
            raise JenkinsNoConnectionError

        if self.server.get_job_name(job_name) is None:
            self.scan_organization(job_name)

        next_build_number = self.server.get_job_info(job_name)[
            'nextBuildNumber']

        self._clean_jenkins_server_crumb()
        queue_item_number = self.server.build_job(
            name=job_name, parameters=parameters)

        method_args = (job_name, queue_item_number,
                       next_build_number, on_complete,)
        threading.Thread(target=self._wait_for_build,
                         daemon=True, args=method_args).start()

    def scan_organization(self, job_name: str = ""):
        org_name = job_name.split("/")[0]
        self._clean_jenkins_server_crumb()

        try:
            self.server.build_job(name=org_name)
        except jenkins.EmptyResponseException as ex:
            logger.warn("Error while scanning organization: {}".format(ex))
        finally:
            time.sleep(5)  # wait for 5 seconds while the scan may still be happening
            # CONSIDER FINDING A WAY OF SCANNING WITHOUT RECEIVING ERRORS
