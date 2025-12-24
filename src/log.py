import logging
import logging.config
import sys

from settings import LOG_LEVEL


def get_logging_config():
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': LOG_LEVEL,
                'formatter': 'standard',
                'stream': sys.stdout,
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': LOG_LEVEL,
                'propagate': True,
            },
        },
    }


def setup_logging():
    config = get_logging_config()
    logging.config.dictConfig(config)
