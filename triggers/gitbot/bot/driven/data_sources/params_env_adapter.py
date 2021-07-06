from bot.driven.repositories import ParamsRepository
from dotenv import load_dotenv
from os.path import join, dirname
import os


class ParamsEnvAdapter(ParamsRepository):

    def __init__(self):
        env_file_path = join(dirname(__file__), '../../../.env')
        if os.getenv('IS_LOCAL', True):
            load_dotenv(env_file_path)

        self.DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
        self.GITHUB_ALLOWED_AUTHORS = os.getenv('GITHUB_ALLOWED_AUTHORS')
        self.GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
        self.JENKINS_URL = os.getenv('JENKINS_URL')
        self.JENKINS_USERNAME = os.getenv('JENKINS_USERNAME')
        self.JENKINS_PASSWORD = os.getenv('JENKINS_PASSWORD')
        self.JENKINS_CONNECTION_TIMEOUT = os.getenv(
            'JENKINS_CONNECTION_TIMEOUT')
        self.JENKINS_READY_TIMEOUT = os.getenv(
            'JENKINS_READY_TIMEOUT')

    def get_discord_token(self):
        return self.DISCORD_TOKEN

    def get_github_allowed_authors(self):
        return self.GITHUB_ALLOWED_AUTHORS

    def get_github_token(self):
        return self.GITHUB_TOKEN

    def get_jenkins_url(self):
        return self.JENKINS_URL

    def get_jenkins_username(self):
        return self.JENKINS_USERNAME

    def get_jenkins_password(self):
        return self.JENKINS_PASSWORD

    def get_jenkins_connection_timeout(self):
        raise self.JENKINS_CONNECTION_TIMEOUT

    def get_jenkins_ready_timeout(self):
        raise self.JENKINS_READY_TIMEOUT
