from .log_print import log_print, LogType
from . import project_config as config
from .error import CellValueError, UserInvokedError
import openpyxl as xl
import datetime
import re


def get_sheets(excel_file_name: str):
    if excel_file_name[-5:] != ".xlsx":
        excel_path = f"{excel_file_name}.xlsx"
    else:
        excel_path = excel_file_name
    try:
        workbook = xl.load_workbook(excel_path)
        sheets = workbook.worksheets
        date_sheet = sheets[0]
        recommend_sheet = sheets[1]

        return [date_sheet, recommend_sheet]
    except Exception as _:
        raise Exception(
            f"파일 {excel_file_name}을 열지 못했습니다. 해당 파일이 정확한 형식의 파일인지 확인한 다음 다시 시도해주세요."
        )


def get_date(sheet):
    year_cell = config.DATE_CELL["year"]
    month_cell = config.DATE_CELL["month"]

    try:
        year = int(sheet[year_cell].value)
        month = int(sheet[month_cell].value)
        date = datetime.date(year, month, 1)
        log_print(
            LogType.SUCCESS, f"{date.year}년 {date.month}월 플레이리스트를 생성합니다."
        )
        return date
    except Exception as e:
        log_print(LogType.ERROR, f"데이터를 가져오는데 실패했습니다.")
        log_print(LogType.ERROR, e)
        log_print(
            LogType.ERROR,
            f"추천하는 법 시트의 {year_cell}셀과 {month_cell}셀에 년도와 월이 제대로 기입되어 있는지 확인해주세요.",
        )
        input("Enter키를 누르면 프로그램이 종료 됩니다...")


def create_file_name(song_name_kor):
    file_name = song_name_kor
    replace_str = '\\/:*?"<>|'
    for char in replace_str:
        file_name = file_name.replace(char, "_")
    return file_name


def get_info(sheet):
    log_print(LogType.PROGRESS, f"엑셀 파일에서 데이터를 가져오는 중입니다...")

    info_array = []
    anon_idx = ord("A")
    file_name_key = config.ADDITIONAL_KEY["파일 이름"]  # 파일 이름에 해당하는 키 이름

    row_idx = config.START_ROW

    try:
        # 다운 가능한 링크가 유튜브가 아닌 정보를 저장
        warned_info = []
        while sheet.cell(row=row_idx, column=1).value is not None:
            info = {}
            person_name = None
            is_warned = False  # 다운가능한 링크가 이상한지
            for idx, key in enumerate(config.EXCEL_KEY.items()):
                cell = sheet.cell(row=row_idx, column=idx + 1)
                prop = key[0]
                key_name = key[1]
                if prop == "이름":
                    person_name = cell.value

                # 필요한 데이터 부분에 이름이 없을 경우 에러 발생
                if prop in config.ESSENTIAL_KEY and cell.value is None:
                    raise CellValueError(person_name, prop)

                # 닉네임이 없을 경우 익명으로 처리
                if prop == "닉네임" and cell.value is None:
                    info[key_name] = "익명" + chr(anon_idx)
                    anon_idx += 1
                # 파일명에 사용할 수 없는 문자 변경
                elif prop == "한국어 노래 제목":
                    file_name = create_file_name(cell.value.strip())
                    info[key_name] = cell.value.strip()
                    info[file_name_key] = file_name
                # 원본 링크가 링크의 형식이 아닐 경우 value를 None으로 처리
                elif prop == "원본 링크":
                    if cell.value is None:
                        info[key_name] = None
                        continue
                    is_valid_link = cell.value.strip().startswith("http")
                    info[key_name] = cell.value if is_valid_link else None
                # 다운로드 가능 링크가 youtube의 링크 형식이 아닐 경우 경고문 출력
                elif prop == "다운로드 가능 링크":
                    yt_link_regex = re.compile(
                        r"^http?s:\/\/(www\.youtube\.com\/watch\?v=|youtu\.be\/)[A-Za-z0-9-_]{11}.*$"
                    )
                    is_valid_link = yt_link_regex.match(cell.value.strip())
                    if not is_valid_link:
                        is_warned = True
                    info[key_name] = cell.value.strip()
                else:
                    info[key_name] = cell.value.strip()
            info_array.append(info)
            if is_warned:
                warned_info.append(info)
            log_print(LogType.SUCCESS, f"{person_name}님의 데이터를 저장했습니다.")
            row_idx += 1

        # 만약 유튜브링크가 아닌 링크가 있다면 사용자에게 알림
        if warned_info:
            log_print(
                LogType.WARNING,
                f"일부 다운로드 가능한 링크가 유튜브 링크가 아닌 것 같습니다.",
            )
            for info in warned_info:
                log_print(
                    LogType.WARNING,
                    f"{info[config.EXCEL_KEY['이름']]}-{info[config.EXCEL_KEY['다운로드 가능 링크']]}",
                )

            user_answer = None

            while user_answer not in ["yes", "no"]:
                user_answer = input(
                    "다운로드를 계속 진행하려면 yes, 중단하려면 no을 입력하고 Enter를 눌러주세요: "
                )
                if user_answer == "no":
                    raise UserInvokedError("사용자가 프로그램을 중단했습니다.")
                elif user_answer == "yes":
                    log_print(LogType.PROGRESS, "다운로드를 계속 진행합니다.")
                    break

        return info_array
    except Exception as _:
        raise


if __name__ == "__main__":
    pass
