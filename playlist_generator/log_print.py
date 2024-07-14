from colorama import Fore, Style


def log_print(log_type, msg):
    if log_type == "성공":
        print(f"{Fore.GREEN}성공:{Style.RESET_ALL}{msg}")
    elif log_type == "작업":
        print(f"{Fore.BLUE}작업:{Style.RESET_ALL}{msg}")
    elif log_type == "오류":
        print(f"{Fore.RED}오류:{Style.RESET_ALL}{msg}")


if __name__ == "__main__":
    pass
