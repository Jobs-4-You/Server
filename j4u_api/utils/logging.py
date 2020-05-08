import logging.config

from j4u_api.config import config


def get_logger(name):
    logging.config.fileConfig(config.LOGGING_CONF_PATH, disable_existing_loggers=False)
    return logging.getLogger(__name__)
