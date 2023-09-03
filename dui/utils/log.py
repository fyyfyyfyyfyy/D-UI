import logging
import os

import colorlog  # type: ignore


def get_logger(filename,
               console_level: str | int = logging.INFO,
               file_level: str | int = logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger(filename)
    logger.setLevel(logging.DEBUG)

    log_directory = "log"

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_file = os.path.join(log_directory, f"{filename}.log")

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(file_level)

    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(console_level)

    formatter_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    file_formatter = logging.Formatter(formatter_string)
    color_formatter = colorlog.ColoredFormatter(
        f'%(log_color)s{formatter_string}',
        log_colors={
            'DEBUG': 'green',
            # 'INFO': 'white',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )

    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(color_formatter)

    # 将处理器添加到logger中
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
