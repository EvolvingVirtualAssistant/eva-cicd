from bot.driven.repositories import JenkinsRepository


class JenkinsService():

    def __init__(self, jenkinsRepository: JenkinsRepository):
        self.jenkinsRepository = jenkinsRepository

    def _get_job_name(prUrl):
        pass

    def _get_job_parameters(prUrl):
        pass

    def trigger_build(self, prUrl: str):
        self.jenkinsRepository.start_jenkins()

        job_name = self._get_job_name(prUrl)
        job_parameters = self._get_job_parameters(prUrl)
        self.jenkinsRepository.trigger_build(job_name, job_parameters)

        # callback to notify of any issue during the process of building a job
        # callback to notify of the test results
        # callback to stop jenkins


# get_nodes
# get_node_info
# node_exists

# get_build_console_output
# quiet_down
# wait_for_normal_op
