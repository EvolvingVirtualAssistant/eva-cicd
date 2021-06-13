from discord.message import Message
from services import DiscordService, JenkinsService
from discord.ext import commands
import re

bot = commands.Bot(command_prefix="!", description="Git Bot")


class DiscordListener():

    def __init__(self, token, discordService: DiscordService, jenkinsService: JenkinsService):
        bot.add_cog(_EventListenerCog(bot, discordService, jenkinsService))

        # this should block here # Replace with this https://stackoverflow.com/questions/66863177/check-if-discord-bot-is-online
        bot.run(token)

        print("Bot shutting down")

    @bot.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(bot))


class _EventListenerCog(commands.Cog):

    def __init__(self, bot: commands.Bot, discordService: DiscordService, jenkinsService: JenkinsService):
        self.bot = bot
        self.discordService = discordService
        self.jenkinsService = jenkinsService

    def _validMessageAuthor(self, message: Message):
        if message.author == self.bot.user:
            return False

        if message.author.bot != True or message.author.name != "GitHub":
            return False

        isGithubAuthorAllowed = False

        if message.embeds is not None and len(message.embeds) > 0 and message.embeds[0].author is not None:
            isGithubAuthorAllowed = message.embeds[0].author.name in [
                'RuiSanches', 'Pedro-Sanches']  # dynamic env var of possible authors

        return isGithubAuthorAllowed

    def _getGithubPrUrl(self, message: Message):
        if (message.embeds is None or len(message.embeds) == 0 or message.embeds[0].url is None):
            return None

        matchedUrl = re.match(".*\/pull\/\d+", message.embeds[0].url)

        if matchedUrl is None:
            return None

        return matchedUrl.group()

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author == self.bot.user:
            return

        print(message)

        if self._validMessageAuthor(message):
            prUrl = self._getGithubPrUrl(message)

            if prUrl is None:
                return  # cehck how to break out of function

            self.jenkinsService.send_message_to_jenkins(prUrl)
            await self.discordService.send_message_to_discord(message.channel, prUrl)
            # check this to interact with github https://pypi.org/project/ghapi/ . Maybe create a github service
