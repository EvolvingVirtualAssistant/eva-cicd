from bot.drivers import DiscordListener
from bot.services import DiscordService, JenkinsService
from bot.driven.data_sources import JenkinsHttpAdapter, ParamsEnvAdapter
import yaml
import logging
import logging.config


def setup_logging():
    with open('logging.yaml', 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)


def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting Bot")

    paramsRepository = ParamsEnvAdapter()
    jenkinsRepository = JenkinsHttpAdapter()

    discordToken = paramsRepository.get_discord_token()

    discordService = DiscordService()
    jenkinsService = JenkinsService(jenkinsRepository)

    discordListener = DiscordListener(discordToken, discordService,
                                      jenkinsService, paramsRepository)
    discordListener.start_listener(True)

    logger.debug("Stopping Bot")


if __name__ == '__main__':
    main()
