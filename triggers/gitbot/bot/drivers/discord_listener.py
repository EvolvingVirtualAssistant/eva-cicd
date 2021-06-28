from bot.services import DiscordService, JenkinsService
from bot.driven.repositories import ParamsRepository
from discord.message import Message
from discord.ext import commands
import asyncio
import re
import threading


class DiscordListener():
    _bot = commands.Bot(command_prefix="!", description="Git Bot")
    _bot_running_lock = threading.Lock()
    _bot_running = False

    def __init__(self, token, discordService: DiscordService, jenkinsService: JenkinsService, paramsRepository: ParamsRepository):
        self._token = token
        if DiscordListener._bot.get_cog("_EventListenerCog") is None:
            DiscordListener._bot.add_cog(_EventListenerCog(DiscordListener._bot, discordService,
                                                           jenkinsService, paramsRepository))

    @_bot.event
    async def on_ready():
        print('Listening to discord')

    def start_listener(self, blocking: bool):
        with DiscordListener._bot_running_lock:
            if DiscordListener._bot_running:
                return

            def _run_bot():
                DiscordListener._bot_running = True
                try:
                    DiscordListener._bot.run(self._token)
                except Exception as ex:
                    print(ex)  # Replace with proper logging
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
                    except Exception:
                        pass  # Ignore exception while closing connection

                try:
                    asyncio.run(_stop_bot())
                except Exception as e:
                    print(e)
                    pass  # Ignore exception while closing connection

                self._listener.join()
                DiscordListener._bot_running = False


class _EventListenerCog(commands.Cog):

    def __init__(self, bot: commands.Bot, discordService: DiscordService, jenkinsService: JenkinsService, paramsRepository: ParamsRepository):
        self._bot = bot
        self._discordService = discordService
        self._jenkinsService = jenkinsService
        self._paramsRepository = paramsRepository

    def _validMessageAuthor(self, message: Message):
        if message.author == self._bot.user:
            return False

        if message.author.bot != True or message.author.name != "GitHub":
            return False

        # is github author allowed
        return (message.embeds is not None and len(message.embeds) > 0 and message.embeds[0].author is not None and
                message.embeds[0].author.name in self._paramsRepository.get_github_allowed_authors())

    def _getGithubPrUrl(self, message: Message):
        if (message.embeds is None or len(message.embeds) == 0 or message.embeds[0].url is None):
            return None

        matchedUrl = re.match(r".*\/pull\/\d+", message.embeds[0].url)

        if matchedUrl is None:
            return None

        return matchedUrl.group()

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if not self._validMessageAuthor(message):
            return

        prUrl = self._getGithubPrUrl(message)

        if prUrl is None:
            return

        self._jenkinsService.send_message_to_jenkins(prUrl)
        await self._discordService.send_message_to_discord(message.channel, prUrl)
        # check this to interact with github https://pypi.org/project/ghapi/ . Maybe create a github service
