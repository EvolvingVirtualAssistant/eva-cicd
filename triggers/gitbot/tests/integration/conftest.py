from bot.driven.data_sources import JenkinsHttpAdapter, ParamsEnvAdapter
from bot.driven.repositories import JenkinsRepository, ParamsRepository
from bot.services import DiscordService, JenkinsService
from bot.drivers import DiscordListener
import pytest


@pytest.fixture
def params_repository() -> ParamsRepository:
    return ParamsEnvAdapter()


@pytest.fixture
def jenkins_repository() -> JenkinsRepository:
    return JenkinsHttpAdapter()


@pytest.fixture
def jenkins_service(jenkins_repository):
    return JenkinsService(jenkins_repository)


@pytest.fixture
def discord_service():
    return DiscordService()


@pytest.fixture
def bot_token(params_repository: ParamsRepository):
    return params_repository.get_discord_token()


@pytest.fixture
def discord_listener(bot_token, discord_service, jenkins_service, params_repository):
    return DiscordListener(bot_token, discord_service, jenkins_service, params_repository)
