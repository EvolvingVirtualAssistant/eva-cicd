from bot.drivers import DiscordListener
from bot.services import DiscordService, JenkinsService
from bot.driven.data_sources import JenkinsHttpAdapter, ParamsEnvAdapter


def main():
    paramsRepository = ParamsEnvAdapter()
    jenkinsRepository = JenkinsHttpAdapter()

    discordToken = paramsRepository.get_discord_token()

    discordService = DiscordService()
    jenkinsService = JenkinsService(jenkinsRepository)

    discordListener = DiscordListener(discordToken, discordService,
                                      jenkinsService, paramsRepository)
    discordListener.start_listener(True)


if __name__ == '__main__':
    main()
