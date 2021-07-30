import asyncio
import logging
import re
import threading
from discord.embeds import EmptyEmbed
from discord.ext import commands
from discord.message import Message
from bot.services import DiscordService, JenkinsService, GithubService
from bot.driven.repositories import ParamsRepository


logger = logging.getLogger(__name__).parent


class DiscordListener():
    _bot = commands.Bot(command_prefix="!", description="Git Bot")
    _bot_running_lock = threading.Lock()
    _bot_running = False

    # pylint: disable=too-many-arguments
    def __init__(self, token, discord_service: DiscordService, jenkins_service: JenkinsService,
                 github_service: GithubService, params_repository: ParamsRepository):
        self._token = token
        self._listener = None
        if DiscordListener._bot.get_cog("_EventListenerCog") is None:
            DiscordListener._bot.add_cog(_EventListenerCog(DiscordListener._bot, discord_service,
                                                           jenkins_service, github_service,
                                                           params_repository))

    # pylint: disable=no-method-argument
    @_bot.event
    async def on_ready():
        logger.info('Listening to discord')

    def start_listener(self, blocking: bool):
        with DiscordListener._bot_running_lock:
            if DiscordListener._bot_running:
                return

            def _run_bot():
                DiscordListener._bot_running = True
                try:
                    DiscordListener._bot.run(self._token)
                except Exception as ex:
                    logger.exception(
                        "Error while starting listener: {}".format(ex))
                finally:
                    DiscordListener._bot_running = False

            if blocking:
                _run_bot()
            else:
                self._listener = threading.Thread(target=_run_bot)
                self._listener.start()

    def stop_listener(self):
        with DiscordListener._bot_running_lock:
            if self._listener is not None:

                async def _stop_bot():
                    try:
                        await DiscordListener._bot.close()
                    except Exception as ex:
                        logger.exception(
                            "Error while stopping listener: {}".format(ex))

                try:
                    asyncio.run(_stop_bot())
                except Exception as ex:
                    logger.exception(
                        "Error while waiting for listener to stop: {}".format(ex))

                self._listener.join()
                DiscordListener._bot_running = False


class _EventListenerCog(commands.Cog):

    # pylint: disable=too-many-arguments
    def __init__(self, bot: commands.Bot, discord_service: DiscordService,
                 jenkins_service: JenkinsService, github_service: GithubService,
                 params_repository: ParamsRepository):
        self._bot = bot
        self._discord_service = discord_service
        self._jenkins_service = jenkins_service
        self._github_service = github_service
        self._params_repository = params_repository

    def _valid_message_author(self, message: Message):
        if message.author == self._bot.user:
            return False

        if message.author.bot is False or message.author.name != "GitHub":
            return False

        # is github author allowed
        return (message.embeds is not None and len(message.embeds) > 0 and
                message.embeds[0].author is not None and
                message.embeds[0].author.name in self._params_repository.get_github_allowed_authors())

    def _get_github_pr_url(self, message: Message):
        if (message.embeds is None or len(message.embeds) == 0 or message.embeds[0].url is None):
            logger.error("Something wrong with the message.embdes content={}".format(message.embeds))
            return None

        if message.embeds[0].url is not EmptyEmbed:
            url = message.embeds[0].url
        else:
            url = message.embeds[0].description

        if re.match(r".*\/commit\/.+", url) is not None:
            url = self._github_service.get_pr_url_from_commit_url(url)
            url = '' if url is None else url
        elif re.match(r".*\/compare\/.+", url) is not None:
            url = self._github_service.get_pr_url_from_compare_url(url)
            url = '' if url is None else url

        matched_url = re.match(r".*\/pull\/\d+", url)

        if matched_url is None:
            logger.error("Unexpected pull url format for={}".format(url))
            return None

        return matched_url.group()

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if not self._valid_message_author(message):
            logger.info("Invalid message author: {}".format(message.author))
            return

        pr_url = self._get_github_pr_url(message)

        if pr_url is None:
            logger.error("Unable to extract pr url from message")
            return

        def _on_build_action(msg, url=None, success=False):
            try:
                self._bot.loop.create_task(self._discord_service.send_status_message_to_discord(
                    message.channel, msg=msg, url=url, success=success))
            except Exception as ex:
                logger.exception(
                    "Error while waiting for sending message to discord: {}".format(ex))

        self._jenkins_service.trigger_build(
            pr_url, _on_build_action, _on_build_action)
