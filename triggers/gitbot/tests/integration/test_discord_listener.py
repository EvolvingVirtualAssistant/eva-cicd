import pytest
from bot.drivers import DiscordListener
import time
import asyncio


def _cleanup_bot_connection():
    # Cleanup bot connection
    try:
        DiscordListener._bot.close
    except Exception:
        pass  # Ignore any exception while closing


def test_event_on_ready(discord_listener: DiscordListener):
    discord_listener.start_listener(False)
    print('Here 0')
    time.sleep(10)
    print('Here 1')
    discord_listener.stop_listener()
    print('Here 2')
    assert False


def test_event_on_messsage(discord_listener):
    pass
