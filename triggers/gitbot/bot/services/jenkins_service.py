from bot.exceptions import JenkinsStartingError, JenkinsStoppingError
from bot.driven.repositories import JenkinsRepository, ParamsRepository
from queue import Queue
from threading import Thread, Timer
import logging
import re


logger = logging.getLogger(__name__).parent


class JenkinsService():

    def __init__(self, jenkins_repository: JenkinsRepository, params_repository: ParamsRepository):
        self._jenkins_repository = jenkins_repository
        self._params_repository = params_repository
        self.queue = Queue(0)
        self.timed_jenkins_shutdown: Timer = None
        self.jenkins_job_runner = Thread(
            target=self._job_runner, daemon=True)
        self.jenkins_job_runner.start()

    def _get_job_name(self, pr_url):
        org_folder = 'GitHub EVA Organization Folder'

        pull_split = re.split(r"\/pull\/", pr_url)
        repo_split = pull_split[0].split("/")

        repo = repo_split[repo_split.__len__()-1]
        pr = 'PR-{}'.format(pull_split[pull_split.__len__()-1])
        return "{}/{}/{}".format(org_folder, repo, pr)

    def _get_job_parameters(self, pr_url):
        return None

    def _start_jenkins_shutdown_timer(self):
        if self.timed_jenkins_shutdown is not None and self.timed_jenkins_shutdown.is_alive():
            self.timed_jenkins_shutdown.cancel()

        self.timed_jenkins_shutdown = Timer(
            self._params_repository.get_jenkins_shutdown_timeout(), self.jenkins_cleanup)
        self.timed_jenkins_shutdown.start()

    def _handle_runner_error(self, pr_url, ex, on_error):
        err_msg = "Error processing job for url: {} -> {}".format(
            pr_url, ex)
        logger.exception(err_msg)
        self._start_jenkins_shutdown_timer()
        on_error(err_msg)

    def _job_runner(self):
        while True:
            try:
                pr_url, on_complete, on_error = self.queue.get()
                job_name = self._get_job_name(pr_url)
                job_parameters = self._get_job_parameters(pr_url)

                if not self._jenkins_repository.is_jenkins_running():
                    self._jenkins_repository.start_jenkins()

                self._jenkins_repository.trigger_build(
                    on_complete, job_name, job_parameters)
            except (JenkinsStartingError, Exception) as ex:
                self._handle_runner_error(pr_url, ex, on_error)
            finally:
                self.queue.task_done()
        # CONSIDER STOPPING JENKINS UPON PROGRAM KILL, SO THAT JENKINS IS NOT ALWAYS RUNNING

    def trigger_build(self, pr_url, on_complete, on_error):
        def _shutdown_on_complete(*args, **kwargs):
            self._start_jenkins_shutdown_timer()
            on_complete(*args, **kwargs)

        self.queue.put_nowait((pr_url, _shutdown_on_complete, on_error))

    def jenkins_cleanup(self):
        try:
            self._jenkins_repository.stop_jenkins()
        except (JenkinsStoppingError, Exception) as ex:
            logger.exception(ex)


# get_nodes
# get_node_info
# node_exists

# get_build_console_output
# quiet_down
# wait_for_normal_op
