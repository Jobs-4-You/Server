import logging.config

from pythonjsonlogger import jsonlogger

from j4u_api.config import config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {"format": "%(asctime)s %(levelname)s %(name)s: %(message)s"},
        "json": {"()": "pythonjsonlogger.jsonlogger.JsonFormatter"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "json",
            "filename": config.LOG_FILE,
            "mode": "a",
            "maxBytes": 500,
            "backupCount": 1,
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}


class Logger:
    @classmethod
    def _log(cls, caller_module, func, *args, **kwargs):
        func_path = f"{func.__module__}.{func.__name__}" if func is not None else ""
        logging.config.dictConfig(LOGGING_CONFIG)
        logger = logging.getLogger(caller_module)
        extra = kwargs.get("extra", {})
        extra["func"] = func_path
        kwargs["extra"] = extra
        return logger, args, kwargs

    @classmethod
    def debug(cls, *args, **kwargs):
        logger, ar, kwar = cls._log(*args, **kwargs)
        logger.debug(*ar, **kwar)

    @classmethod
    def info(cls, *args, **kwargs):
        logger, ar, kwar = cls._log(*args, **kwargs)
        logger.info(*ar, **kwar)

    @classmethod
    def warning(cls, *args, **kwargs):
        logger, ar, kwar = cls._log(*args, **kwargs)
        logger.warning(*ar, **kwar)

    @classmethod
    def error(cls, *args, **kwargs):
        logger, ar, kwar = cls._log(*args, **kwargs)
        logger.error(*ar, **kwar)

    @classmethod
    def critical(cls, *args, **kwargs):
        logger, ar, kwar = cls._log(*args, **kwargs)
        logger.critical(*ar, **kwar)

    @classmethod
    def exception(cls, *args, **kwargs):
        logger, ar, kwar = cls._log(*args, **kwargs)
        logger.exception(*ar, **kwar)


logger = Logger()
