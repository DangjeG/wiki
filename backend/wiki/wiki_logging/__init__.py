import json
import logging
import sys
from datetime import datetime
from logging.config import dictConfig

import stackprinter

from wiki.config import settings
from wiki.wiki_logging.schemas import BaseLogSchema


LEVEL_TO_NAME = {
    logging.CRITICAL: "CRITICAL",
    logging.ERROR: "ERROR",
    logging.WARNING: "WARNING",
    logging.INFO: "INFO",
    logging.DEBUG: "DEBUG",
    logging.NOTSET: "TRACE",
}


class JSONLogFormatter(logging.Formatter):
    """
    Custom class-formatter for writing logs to json
    """

    def format(self, record: logging.LogRecord, *args, **kwargs) -> str:
        """
        Formatting LogRecord to json

        :param record: logging.LogRecord
        :return: json string
        """
        log_object: dict = self._format_log_object(record)
        return json.dumps(log_object, ensure_ascii=False)

    @staticmethod
    def _format_log_object(record: logging.LogRecord) -> dict:
        now = (
            datetime.
            fromtimestamp(record.created).
            astimezone().
            replace(microsecond=0).
            isoformat()
        )
        message = record.getMessage()
        duration = (
            record.duration
            if hasattr(record, "duration")
            else record.msecs
        )

        json_log_fields = BaseLogSchema(
            name=record.name,
            level_name=LEVEL_TO_NAME[record.levelno],
            module=record.module,
            func_name=record.funcName,
            filename=record.filename,
            pathname=record.pathname,
            timestamp=now,
            thread_id=record.thread,
            process_id=record.process,
            message=message,
            app_name=settings.PROJECT_NAME,
            app_version=settings.VERSION,
            app_env=settings.ENVIRONMENT,
            duration=duration
        )

        if record.exc_info:
            json_log_fields.exceptions = (
                # default library traceback
                # traceback.format_exception(*record.exc_info)

                # stackprinter gets all debug information
                # https://github.com/cknd/stackprinter/blob/master/stackprinter/__init__.py#L28-L137
                stackprinter.format(
                    record.exc_info,
                    suppressed_paths=[
                        r"lib/python.*/site-packages/starlette.*",
                        ],
                    add_summary=False,
                    ).split("\n")
            )

        elif record.exc_text:
            json_log_fields.exceptions = record.exc_text

        # Pydantic to dict
        json_log_object = json_log_fields.model_dump(
            exclude_unset=True,
            by_alias=True,
        )

        return json_log_object


def handlers(env,
             *,
             to_file: bool = False):
    if env.lower() in ("dev", "local"):
        handler = ["console"]
    else:
        handler = ["intercept"]

    if to_file:
        handler.append("file_handler")

    return handler


LOG_HANDLER = handlers(settings.ENVIRONMENT,
                       to_file=True)
LOGGING_LEVEL = logging.DEBUG if settings.DEBUG else logging.INFO

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "standard": {
            "format": "%(asctime)s - [%(levelname)s] %(name)s [%(module)s.%(funcName)s:%(lineno)d]: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "json": {
            "()": JSONLogFormatter,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": sys.stdout,
        },
        "file_handler": {
            "level": "INFO",
            "filename": settings.LOG_FILENAME,
            "class": "logging.FileHandler",
            "formatter": "json"
        }
    },
    "loggers": {
        "uvicorn": {
            "handlers": LOG_HANDLER,
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": LOG_HANDLER,
            "level": "ERROR",
            "propagate": False,
        },
    },
    "root": {
        "handlers": LOG_HANDLER,
        "level": "INFO",
        "propagate": False,
    },
}


def setup_logging():
    dictConfig(LOG_CONFIG)
