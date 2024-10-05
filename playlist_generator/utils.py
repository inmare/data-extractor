import time


def get_current_time() -> str:
    """
    현재 시간을 반환하는 함수

    Returns:
        str: mmdd HHMMSS 형태의 현재 시간
    """
    return time.strftime("%m-%d %H-%M-%S", time.localtime())


if __name__ == "__main__":
    pass
