import sys
from drivers import DiscordListener
from services import DiscordService, JenkinsService
from driven.data_sources import JenkinsHttpAdapter


def _getDiscordToken() -> str:
    print("Token: %s" % sys.argv[1])
    return sys.argv[1]


def main():
    token = _getDiscordToken()

    jenkinsRepository = JenkinsHttpAdapter()

    discordService = DiscordService()
    jenkinsService = JenkinsService(jenkinsRepository)

    discordListener = DiscordListener(token, discordService, jenkinsService)


if __name__ == '__main__':
    main()
