import json
from os.path import abspath, join, dirname
from types import SimpleNamespace
from unittest.mock import MagicMock
import pytest
from discord.message import Message
from bot.driven.data_sources import JenkinsHttpAdapter, ParamsEnvAdapter
from bot.driven.repositories import JenkinsRepository, ParamsRepository
from bot.services import DiscordService, JenkinsService, GithubService
from bot.drivers.discord_listener import _EventListenerCog
from bot.drivers import DiscordListener


# pylint: disable=redefined-outer-name


@pytest.fixture
def params_repository() -> ParamsRepository:
    return ParamsEnvAdapter()


@pytest.fixture
def jenkins_repository(params_repository) -> JenkinsRepository:
    return JenkinsHttpAdapter(params_repository)


@pytest.fixture
def jenkins_service(jenkins_repository, params_repository):
    return JenkinsService(jenkins_repository, params_repository)


@pytest.fixture
def discord_service():
    return DiscordService()


@pytest.fixture
def github_service(params_repository):
    return GithubService(params_repository)


@pytest.fixture
def bot_token(params_repository: ParamsRepository):
    return params_repository.get_discord_token()


@pytest.fixture
def discord_listener(bot_token, discord_service, jenkins_service, github_service, params_repository):
    return DiscordListener(
        bot_token, discord_service, jenkins_service, github_service, params_repository)


@pytest.fixture
def discord_internal_bot():
    DiscordListener._bot = MagicMock()
    return DiscordListener._bot


@pytest.fixture
def discord_event_listener_cog(discord_internal_bot, discord_service, jenkins_service, github_service, params_repository):
    return _EventListenerCog(discord_internal_bot, discord_service, jenkins_service, github_service, params_repository)


@pytest.fixture
def sample_message():
    file = abspath(join(dirname(__file__), '../resources/sample_message.json'))
    with open(file, 'r') as sample:
        msg: Message = json.load(
            sample, object_hook=lambda d: SimpleNamespace(**d))
    return msg


@pytest.fixture
def mock_any_arg():
    # pylint: disable=too-few-public-methods
    class MockAnyArg():
        def __eq__(self, o: object) -> bool:
            return True
    return MockAnyArg()
