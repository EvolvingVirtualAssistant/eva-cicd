class DiscordService():

    def __init__(self):
        pass

    async def send_message_to_discord(self, channel, msg: str):
        await channel.send(msg)
