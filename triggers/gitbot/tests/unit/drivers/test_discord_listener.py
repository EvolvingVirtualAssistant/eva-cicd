
import time
import threading
from discord.ext.commands.bot import Bot
import pytest
from unittest.mock import MagicMock
from bot.drivers import DiscordListener


"""Testing listener starting and stoping functionalities"""


def wait_for_assertion(assertion):
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

    wait_for_assertion(discord_internal_bot.run.assert_called)
    assert DiscordListener._bot_running == True
    stop_running = True
    test_thread.join()
    wait_for_assertion(assert_bot_not_running)


def test_non_blocking_listener(discord_listener: DiscordListener, discord_internal_bot: Bot):
    stop_running = False

    def mock_run(token):
        while not stop_running:
            time.sleep(1)
        return

    def stop_mock_run():
        nonlocal stop_running
        stop_running = True

    discord_internal_bot.run = MagicMock(side_effect=mock_run)
    discord_internal_bot.close = MagicMock(side_effect=stop_mock_run)

    discord_listener.start_listener(False)

    wait_for_assertion(discord_internal_bot.run.assert_called)
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

    def stop_mock_run():
        nonlocal stop_running
        stop_running = True

    discord_internal_bot.run = MagicMock(side_effect=mock_run)
    discord_internal_bot.close = MagicMock(side_effect=stop_mock_run)

    discord_listener.start_listener(False)

    wait_for_assertion(discord_internal_bot.run.assert_called)
    assert DiscordListener._bot_running == True
    assert n_runs == 1
    discord_listener.start_listener(False)
    assert n_runs == 1

    discord_listener.stop_listener()
    discord_internal_bot.close.assert_called
    assert DiscordListener._bot_running == False


def test_event_on_ready(discord_listener: DiscordListener):
    # Don't think we need to test this event for now
    pass


"""Testing listener specific message handling"""


def test_event_on_message(discord_listener: DiscordListener):
    pass
