import logging
import logging.config
import yaml
from bot.drivers import DiscordListener
from bot.services import DiscordService, JenkinsService, GithubService
from bot.driven.data_sources import JenkinsHttpAdapter, ParamsEnvAdapter


def setup_logging():
    with open('logging.yaml', 'r') as file:
        config = yaml.safe_load(file.read())
        logging.config.dictConfig(config)


def main():
    setup_logging()
    logger = logging.getLogger()
    logger.info("Starting Bot")

    params_repository = ParamsEnvAdapter()
    jenkins_repository = JenkinsHttpAdapter(params_repository)

    discord_token = params_repository.get_discord_token()

    discord_service = DiscordService()
    jenkins_service = JenkinsService(jenkins_repository, params_repository)
    github_service = GithubService(params_repository)

    discord_listener = DiscordListener(discord_token, discord_service,
                                       jenkins_service, github_service, params_repository)
    discord_listener.start_listener(True)

    logger.debug("Stopping Bot")


if __name__ == '__main__':
    main()
