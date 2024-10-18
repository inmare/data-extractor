import logging
from colorama import Fore, Style

LoggerColor = {
    logging.DEBUG: Fore.BLUE,
    logging.INFO: Fore.GREEN,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Fore.MAGENTA,
}

LoggerMsg = {
    logging.DEBUG: "작업",
    logging.INFO: "정보",
    logging.WARNING: "경고",
    logging.ERROR: "오류",
    logging.CRITICAL: "심각한 오류",
}


class ColoredFormatter(logging.Formatter):
    def format(self, record: logging):
        level_color = LoggerColor.get(record.levelno, Fore.WHITE)
        level_msg = LoggerMsg.get(record.levelno, "알 수 없는 메세지")
        record.msg = (
            f"{level_color}{level_msg} - {Fore.WHITE}{record.msg}{Style.RESET_ALL}"
        )
        return super().format(record)


def _init_logger():
    logger = logging.getLogger("playlist_generator")
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = ColoredFormatter("%(asctime)s - %(message)s", datefmt="%H:%M:%S")
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


if __name__ == "__main__":
    pass
