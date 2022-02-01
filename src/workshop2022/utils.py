import logging


def setup_logging(log_level = logging.INFO) -> None:
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'level': log_level,
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': log_level,
                'propagate': True
            },
        }
    }
    logging.config.dictConfig(config)
    logging.info('Initiated with config')
    logging.debug('Logging config: %s', config)
