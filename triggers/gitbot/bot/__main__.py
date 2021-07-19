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
    logger = logging.getLogger()
    logger.info("Starting Bot")

    params_repository = ParamsEnvAdapter()
    jenkins_repository = JenkinsHttpAdapter(params_repository)

    discord_token = params_repository.get_discord_token()

    discord_service = DiscordService()
    jenkins_service = JenkinsService(jenkins_repository)

    discord_listener = DiscordListener(discord_token, discord_service,
                                       jenkins_service, params_repository)
    discord_listener.start_listener(True)

    logger.debug("Stopping Bot")


if __name__ == '__main__':
    main()
