"""Logging configuration."""

import logging
import sys

from colorama import Fore, Style


class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA,
    }

    def format(self, record):
        base = super().format(record)
        color = self.COLORS.get(record.levelno, "")
        return f"{color}{base}{Style.RESET_ALL}"


def setup_logger(name: str = "gotcha", quiet: bool = False):
    logger = logging.getLogger(name)
    logger.setLevel(logging.WARNING if quiet else logging.INFO)
    logger.handlers.clear()
    logger.propagate = False

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(ColorFormatter("[%(levelname)s] %(message)s"))
    logger.addHandler(handler)
    return logger
