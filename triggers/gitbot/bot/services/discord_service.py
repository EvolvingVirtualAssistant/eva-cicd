from discord import Embed
from discord.colour import Color


class DiscordService():

    def __init__(self):
        pass

    async def send_message_to_discord(self, channel, msg: str):
        await channel.send(msg)

    async def send_success_message_to_discord(self, channel, msg: str, url=None):
        embed = Embed(description=msg, url=url, colour=Color.green())
        await channel.send(embed=embed)

    async def send_fail_message_to_discord(self, channel, msg: str, url=None):
        embed = Embed(description=msg, url=url, colour=Color.red())
        await channel.send(embed=embed)
