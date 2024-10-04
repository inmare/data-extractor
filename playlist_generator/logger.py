import logging
from colorama import Fore, Style

LoggerColor = {
    logging.DEBUG: Fore.BLUE,  # DEBUG: 초록색
    logging.INFO: Fore.GREEN,  # INFO: 파란색
    logging.WARNING: Fore.YELLOW,  # WARNING: 노란색
    logging.ERROR: Fore.RED,  # ERROR: 빨간색
    logging.CRITICAL: Fore.MAGENTA,  # CRITICAL: 자홍색
}


class ColoredFormatter(logging.Formatter):
    def format(self, record: logging):
        level_color = LoggerColor.get(record.levelno, Fore.WHITE)
        record.msg = f"{level_color}{record.levelname} - {Fore.WHITE}{record.msg}{Style.RESET_ALL}"
        return super().format(record)


def _init_logger():
    logger = logging.getLogger("playlist_generator")
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = ColoredFormatter('%(asctime)s - %(message)s', datefmt='%H:%M:%S')
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    return logger


class Logger:
    logger = _init_logger()

    @classmethod
    def debug(cls, msg: str):
        cls.logger.debug(msg)

    @classmethod
    def info(cls, msg: str):
        cls.logger.info(msg)

    @classmethod
    def warning(cls, msg: str):
        cls.logger.warning(msg)

    @classmethod
    def error(cls, msg: str):
        cls.logger.error(msg)


# from enum import Enum, auto
#
#
# class LogType(Enum):
#     ERROR = auto()
#     WARNING = auto()
#     SUCCESS = auto()
#     PROGRESS = auto()
#
#
# def log_print(log_type, msg):
#     if log_type == LogType.SUCCESS:
#         print(f"{Fore.GREEN}성공:{Style.RESET_ALL}{msg}")
#     elif log_type == LogType.PROGRESS:
#         print(f"{Fore.BLUE}작업:{Style.RESET_ALL}{msg}")
#     elif log_type == LogType.ERROR:
#         print(f"{Fore.RED}오류:{Style.RESET_ALL}{msg}")
#     elif log_type == LogType.WARNING:
#         print(f"{Fore.YELLOW}경고:{Style.RESET_ALL}{msg}")


if __name__ == "__main__":
    pass
