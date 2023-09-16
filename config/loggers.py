import logging
from termcolor import colored


class LoggingSetup(logging.Formatter):
    COLORS = {
        "INFO": "white",
        "DEBUG": "cyan",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red",
    }

    def format(self, record):
        log_message = super().format(record)
        return colored(log_message, self.COLORS.get(record.levelname))

    def setup_logging(self, debug=False):
        formatter = "%(asctime)s - %(levelname)s: %(message)s"
        level = logging.DEBUG if debug else logging.INFO
        logger = logging.getLogger()
        handler = logging.StreamHandler()
        handler.setFormatter(LoggingSetup(formatter))
        logger.addHandler(handler)
        logger.setLevel(level)
