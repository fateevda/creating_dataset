__doc__ = """
Вспомогательные функции, общие для разных модулей.
"""

import sys
import logging
from pathlib import Path


def setup_logger(logger: logging.Logger, path: [str, Path]):
    """Настраиваем логирование."""
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter('{asctime}: {levelname}: {message}',
                            datefmt='%Y-%m-%d %H:%M:%S', style='{')

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(fmt)
    logger.addHandler(stdout_handler)

    file_handler = logging.FileHandler(path)
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)