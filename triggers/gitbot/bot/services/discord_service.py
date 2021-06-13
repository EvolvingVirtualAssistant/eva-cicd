class DiscordService():

    def __init__(self):
        pass

    async def send_message_to_discord(self, channel, prUrl: str):
        await channel.send(prUrl)
