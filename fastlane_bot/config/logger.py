"""
Fastlane bot config -- logger
"""
__VERSION__ = "0.9"
__DATE__ = "26/Apr 2023"
from .base import ConfigBase
from . import selectors as S
# import os
# from dotenv import load_dotenv
# load_dotenv()
# from decimal import Decimal
import logging

class ConfigLogger(ConfigBase):
    """
    Fastlane bot config -- logger
    """
    __VERSION__=__VERSION__
    __DATE__=__DATE__
    LOGGER_DEFAULT = S.LOGGER_DEFAULT
    LOGLEVEL_DEBUG = S.LOGLEVEL_DEBUG
    LOGLEVEL_INFO = S.LOGLEVEL_INFO
    LOGLEVEL_WARNING = S.LOGLEVEL_WARNING
    LOGLEVEL_ERROR = S.LOGLEVEL_ERROR
    
    def get_logger(self, loglevel: str) -> logging.Logger:
        """
        Returns a logger with the specified logging level

        Args:
            loglevel (str): The desired logging level.

        Returns:
            logging.Logger: A logger object with the specified logging level.
        """
        log_level = getattr(logging, loglevel.upper())
        logger = logging.getLogger("fastlane")
        logger.setLevel(log_level)
        handler = logging.StreamHandler()
        handler.setLevel(log_level)
        formatter = logging.Formatter(
            "%(asctime)s [%(name)s:%(levelname)s] - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    
    def logger(self, *args, **kwargs):
        """placeholder; raise NotImplementedError"""
        raise NotImplementedError("logger() method not implemented")
    
    @classmethod
    def new(cls, logger=None, **kwargs):
        """
        Return a new ConfigLogger.
        """
        if logger is None:
            logger = S.LOGGER_DEFAULT
        
        if logger == S.LOGGER_DEFAULT:
            return _ConfigLoggerDefault(**kwargs)
        else:
            raise ValueError(f"Unknown logger: {logger}")
        
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)


class _ConfigLoggerDefault(ConfigLogger):
    """
    Fastlane bot config -- logger
    """

    LOGLEVEL = "INFO"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = self.get_logger(self.LOGLEVEL)
    
