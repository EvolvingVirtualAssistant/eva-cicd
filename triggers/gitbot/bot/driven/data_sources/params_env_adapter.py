import os
from os.path import join, dirname
from dotenv import load_dotenv
from bot.driven.repositories import ParamsRepository


class ParamsEnvAdapter(ParamsRepository):

    # pylint: disable=too-many-instance-attributes

    def __init__(self):
        env_file_path = join(dirname(__file__), '../../../.env')
        if os.getenv('IS_LOCAL', 'True') == 'True':
            load_dotenv(env_file_path)

        self.discord_token = os.getenv('DISCORD_TOKEN')
        self.github_allowed_authors = os.getenv('GITHUB_ALLOWED_AUTHORS')
        self.github_api_token = os.getenv('GITHUB_API_TOKEN')
        self.github_organization = os.getenv('GITHUB_ORGANIZATION')
        self.jenkins_url = os.getenv('JENKINS_URL')
        self.jenkins_username = os.getenv('JENKINS_USERNAME')
        self.jenkins_password = os.getenv('JENKINS_PASSWORD')
        self.jenkins_connection_timeout = int(os.getenv(
            'JENKINS_CONNECTION_TIMEOUT'))
        self.jenkins_ready_timeout = int(os.getenv(
            'JENKINS_READY_TIMEOUT'))
        self.jenkins_all_nodes_online_timeout = int(os.getenv(
            'JENKINS_ALL_NODES_ONLINE_TIMEOUT'))
        self.jenkins_shutdown_timeout = int(
            os.getenv('JENKINS_SHUTDOWN_TIMEOUT'))

    def get_discord_token(self):
        return self.discord_token

    def get_github_allowed_authors(self):
        return self.github_allowed_authors

    def get_github_api_token(self):
        return self.github_api_token

    def get_github_organization(self):
        return self.github_organization

    def get_jenkins_url(self):
        return self.jenkins_url

    def get_jenkins_username(self):
        return self.jenkins_username

    def get_jenkins_password(self):
        return self.jenkins_password

    def get_jenkins_connection_timeout(self):
        return self.jenkins_connection_timeout

    def get_jenkins_ready_timeout(self):
        return self.jenkins_ready_timeout

    def get_jenkins_all_nodes_online_timeout(self):
        return self.jenkins_all_nodes_online_timeout

    def get_jenkins_shutdown_timeout(self):
        return self.jenkins_shutdown_timeout
