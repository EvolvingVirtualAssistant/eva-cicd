from discord.ext.commands.bot import Bot
from unittest.mock import MagicMock
from bot.drivers.discord_listener import _EventListenerCog
from bot.drivers import DiscordListener
import asyncio
import logging
import pytest
import re
import time
import threading


logger = logging.getLogger(__name__)

"""Testing listener starting and stoping functionalities"""


def _wait_for_assertion(assertion):
    # add timeout mechanism
    is_assertion_false = True
    while is_assertion_false:
        try:
            assertion()
            is_assertion_false = False
        except AssertionError:
            time.sleep(1)


def test_blocking_listener(discord_listener: DiscordListener, discord_internal_bot: Bot):
    stop_running = False

    def mock_run(token):
        while not stop_running:
            time.sleep(1)
        return

    def assert_bot_not_running():  # How can I make this generic????
        assert DiscordListener._bot_running == False

    discord_internal_bot.run = MagicMock(side_effect=mock_run)

    test_thread = threading.Thread(
        target=discord_listener.start_listener, args=[True])
    test_thread.start()

    _wait_for_assertion(discord_internal_bot.run.assert_called)
    assert DiscordListener._bot_running == True
    stop_running = True
    test_thread.join()
    _wait_for_assertion(assert_bot_not_running)


def test_non_blocking_listener(discord_listener: DiscordListener, discord_internal_bot: Bot):
    stop_running = False

    def mock_run(token):
        while not stop_running:
            time.sleep(1)
        return

    async def stop_mock_run():
        nonlocal stop_running
        stop_running = True

    discord_internal_bot.run = MagicMock(side_effect=mock_run)
    discord_internal_bot.close = MagicMock(side_effect=stop_mock_run)

    discord_listener.start_listener(False)

    _wait_for_assertion(discord_internal_bot.run.assert_called)
    assert DiscordListener._bot_running == True
    discord_listener.stop_listener()
    discord_internal_bot.close.assert_called
    assert DiscordListener._bot_running == False


def test_only_one_listener_at_a_time(discord_listener: DiscordListener, discord_internal_bot: Bot):
    stop_running = False
    n_runs = 0

    def mock_run(token):
        nonlocal n_runs
        n_runs += 1
        while not stop_running:
            time.sleep(1)
        return

    async def stop_mock_run():
        nonlocal stop_running
        stop_running = True

    discord_internal_bot.run = MagicMock(side_effect=mock_run)
    discord_internal_bot.close = MagicMock(side_effect=stop_mock_run)

    discord_listener.start_listener(False)

    _wait_for_assertion(discord_internal_bot.run.assert_called)
    assert DiscordListener._bot_running == True
    assert n_runs == 1
    discord_listener.start_listener(False)
    assert n_runs == 1

    discord_listener.stop_listener()
    discord_internal_bot.close.assert_called
    assert DiscordListener._bot_running == False


"""Testing listener specific message handling"""


def _call_on_message(discord_event_listener_cog: _EventListenerCog, sample_message):
    try:
        asyncio.run(discord_event_listener_cog.on_message(sample_message))
    except Exception as ex:
        logger.exception("Test error on message:")
        assert False


def _invalid_author_sample_message(sample_message, author_name, author_is_bot, embeds):
    sample_message.author.name = author_name
    sample_message.author.bot = author_is_bot
    sample_message.embeds = embeds
    return sample_message


def _change_embeds_author(sample_message, author):
    sample_message.embeds[0].author = author
    return sample_message.embeds


def _change_embeds_author_name(sample_message, author_name):
    sample_message.embeds[0].author.name = author_name
    return sample_message.embeds


@pytest.mark.parametrize("change_msg, get_bot_user", [
    (lambda msg: _invalid_author_sample_message(msg, "Discord bot", True, None),
     lambda msg: _invalid_author_sample_message(msg, "Discord bot", True, None).author),
    (lambda msg: _invalid_author_sample_message(
        msg, "GitHub", False, None), lambda msg: None),
    (lambda msg: _invalid_author_sample_message(
        msg, "notGitHub", True, None), lambda msg: None),
    (lambda msg: _invalid_author_sample_message(
        msg, "notGitHub", False, None), lambda msg: None),
    (lambda msg: _invalid_author_sample_message(
        msg, "GitHub", True, None), lambda msg: None),
    (lambda msg: _invalid_author_sample_message(
        msg, "GitHub", True, []), lambda msg: None),
    (lambda msg: _invalid_author_sample_message(msg, "GitHub",
                                                True, _change_embeds_author(msg, None)), lambda msg: None),
    (lambda msg: _invalid_author_sample_message(msg, "GitHub", True,
                                                _change_embeds_author_name(msg, "notInAllowedAuthors")), lambda msg: None)
])
def test_event_on_message_invalid_author(discord_event_listener_cog: _EventListenerCog, sample_message, change_msg, get_bot_user):
    msg = change_msg(sample_message)
    discord_event_listener_cog._bot.user = get_bot_user(sample_message)
    discord_event_listener_cog._paramsRepository.get_github_allowed_authors = MagicMock(
        return_value=["Test"])
    discord_event_listener_cog._jenkinsService.send_message_to_jenkins = MagicMock()
    discord_event_listener_cog._discordService.send_message_to_discord = MagicMock()

    _call_on_message(discord_event_listener_cog, msg)

    discord_event_listener_cog._jenkinsService.send_message_to_jenkins.assert_not_called()
    discord_event_listener_cog._discordService.send_message_to_discord.assert_not_called()


def _invalid_pr_url(samples_message, embeds):
    samples_message.embeds = embeds
    return samples_message


def _change_embeds_url(samples_message, url):
    samples_message.embeds[0].url = url
    return samples_message.embeds


@pytest.mark.parametrize("change_msg", [
    (lambda msg: _invalid_pr_url(msg, None)),
    (lambda msg: _invalid_pr_url(msg, [])),
    (lambda msg: _invalid_pr_url(msg, _change_embeds_url(msg, None))),
    (lambda msg: _invalid_pr_url(msg, _change_embeds_url(
        msg, "https://github.com/EvolvingVirtualAssistant/eva-cicd/unmatching-pr-url/a")))
])
def test_event_on_message_invalid_pr_url(discord_event_listener_cog: _EventListenerCog, sample_message, change_msg):
    msg = change_msg(sample_message)
    discord_event_listener_cog._paramsRepository.get_github_allowed_authors = MagicMock(
        return_value=["Test"])
    discord_event_listener_cog._jenkinsService.send_message_to_jenkins = MagicMock()
    discord_event_listener_cog._discordService.send_message_to_discord = MagicMock()

    _call_on_message(discord_event_listener_cog, msg)

    discord_event_listener_cog._jenkinsService.send_message_to_jenkins.assert_not_called()
    discord_event_listener_cog._discordService.send_message_to_discord.assert_not_called()


def test_event_on_message(discord_event_listener_cog: _EventListenerCog, sample_message):
    async def mock_send_message_to_discord(channel, prUrl):
        pass

    discord_event_listener_cog._paramsRepository.get_github_allowed_authors = MagicMock(
        return_value=["Test"])
    discord_event_listener_cog._jenkinsService.send_message_to_jenkins = MagicMock()
    discord_event_listener_cog._discordService.send_message_to_discord = MagicMock(
        side_effect=mock_send_message_to_discord)
    url = re.match(r".*\/pull\/\d+", sample_message.embeds[0].url).group()

    _call_on_message(discord_event_listener_cog, sample_message)

    discord_event_listener_cog._jenkinsService.send_message_to_jenkins.assert_called_with(
        url)
    discord_event_listener_cog._discordService.send_message_to_discord.assert_called_with(
        sample_message.channel, url)
