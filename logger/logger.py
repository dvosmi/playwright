import logging
import os.path
import sys
from logging.handlers import RotatingFileHandler
from typing import Union

from logger.logger_config import LoggerConfig


class Logger:
    if not os.path.isdir(LoggerConfig.LOGS_DIR_NAME):
        os.makedirs(LoggerConfig.LOGS_DIR_NAME)

    logger = logging.getLogger(LoggerConfig.LOGGER_NAME)
    logger.setLevel(LoggerConfig.LOGS_LEVEL)

    formatter = logging.Formatter(LoggerConfig.FORMAT)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        LoggerConfig.LOGS_FILE_NAME, maxBytes=LoggerConfig.MAX_BYTES, backupCount=LoggerConfig.BACKUP_COUNT
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    @staticmethod
    def set_level(level: Union[str, int]) -> None:
        Logger.logger.setLevel(level)

    @staticmethod
    def info(message: str) -> None:
        Logger.logger.info(msg=message)

    @staticmethod
    def debug(message: str) -> None:
        Logger.logger.debug(msg=message)
