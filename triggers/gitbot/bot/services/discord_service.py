from discord import Embed
from discord.colour import Color


class DiscordService():

    def __init__(self):
        pass

    async def send_message_to_discord(self, channel, msg: str):
        await channel.send(msg)

    async def send_status_message_to_discord(self, channel, msg: str, url=None, success=False):
        color = Color.green() if success else Color.red()
        embed = Embed(description=msg, url=url, colour=color)
        await channel.send(embed=embed)
