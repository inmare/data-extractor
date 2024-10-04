# class CellValueError(Exception):
#     def __init__(self, person, prop):
#         self.msg = f"{person}님의 {prop}에 해당하는 정보가 없는 것 같습니다. 엑셀 파일을 확인해주세요."

#     def __str__(self):
#         return self.msg


# class UserInvokedError(Exception):
#     def __init__(self, msg):
#         self.msg = msg

#     def __str__(self):
#         return self.msg


class UserInvokedException(Exception):
    """
    유저가 스스로 프로그램을 종료했을 때 발생하는 에러메세지
    """
    def __init__(self) -> None:
        self.msg = "사용자가 프로그램을 종료했습니다."

    def __str__(self) -> str:
        return self.msg


class CustomException(Exception):
    """
    사용자가 정의한 에러클래스
    해당 에러가 발생하면 사용자에게 메시지를 출력하고 프로그램을 종료한다.
    만약 예상하지 못한 에러가 발생한다면 그 에러의 메세지를 그대로 출력한다.
    """

    def __init__(self, msg: str) -> None:
        """
        에러클래스 생성자

        :param msg: 에러 메시지
        """
        self.msg = msg

    def __str__(self) -> str:
        return self.msg


if __name__ == "__main__":
    pass
