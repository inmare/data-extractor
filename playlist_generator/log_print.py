from colorama import Fore, Style
from enum import Enum, auto


class LogType(Enum):
    ERROR = auto()
    WARNING = auto()
    SUCCESS = auto()
    PROGRESS = auto()


def log_print(log_type, msg):
    if log_type == LogType.SUCCESS:
        print(f"{Fore.GREEN}성공:{Style.RESET_ALL}{msg}")
    elif log_type == LogType.PROGRESS:
        print(f"{Fore.BLUE}작업:{Style.RESET_ALL}{msg}")
    elif log_type == LogType.ERROR:
        print(f"{Fore.RED}오류:{Style.RESET_ALL}{msg}")
    elif log_type == LogType.WARNING:
        print(f"{Fore.YELLOW}경고:{Style.RESET_ALL}{msg}")


if __name__ == "__main__":
    pass
