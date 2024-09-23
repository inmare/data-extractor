class CellValueError(Exception):
    def __init__(self, person, prop):
        self.msg = f"{person}님의 {prop}에 해당하는 정보가 없는 것 같습니다. 엑셀 파일을 확인해주세요."

    def __str__(self):
        return self.msg


class UserInvokedError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


if __name__ == "__main__":
    pass
