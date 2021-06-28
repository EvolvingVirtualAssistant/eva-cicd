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

    def get_discord_token(self):
        return self.DISCORD_TOKEN

    def get_github_allowed_authors(self):
        return self.GITHUB_ALLOWED_AUTHORS

    def get_github_token(self):
        return self.GITHUB_TOKEN
