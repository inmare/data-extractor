from .log_print import log_print, LogType
from . import project_config as config
import openpyxl as xl
import datetime
import sys


def get_sheets(excel_file_name: str):
    if excel_file_name[-5:] != ".xlsx":
        excel_path = f"{excel_file_name}.xlsx"
    else:
        excel_path = excel_path
    try:
        workbook = xl.load_workbook(excel_path)
        sheets = workbook.worksheets
        date_sheet = sheets[0]
        recommend_sheet = sheets[1]

        return [date_sheet, recommend_sheet]
    except Exception as e:
        log_print(
            LogType.ERROR,
            f"엑셀 파일을 열지 못했습니다. 파일이 업로드 되었는지, 이름은 제대로 입력했는지 확인해주세요.",
        )
        sys.exit(0)


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
            f"추천하는 법 시트의 {year_cell}과 {month_cell}에 년도와 월이 제대로 기입되어 있는지 확인해주세요.",
        )
        sys.exit(0)


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
        while sheet.cell(row=row_idx, column=1).value is not None:
            info = {}
            person_name = None
            for idx, key in enumerate(config.EXCEL_KEY.items()):
                cell = sheet.cell(row=row_idx, column=idx + 1)
                property = key[0]
                key_name = key[1]
                if property == "이름":
                    person_name = cell.value

                # 필요한 데이터 부분에 이름이 없을 경우 에러 발행
                if property in config.ESSENTIAL_KEY and cell.value is None:
                    raise Exception(person_name, property)

                # 닉네임이 없을 경우 익명으로 처리
                if property == "닉네임" and cell.value is None:
                    info[key_name] = "익명" + chr(anon_idx)
                    anon_idx += 1
                # 파일명에 사용할 수 없는 문자 변경
                elif property == "한국어 노래 제목":
                    file_name = create_file_name(cell.value)
                    info[key_name] = cell.value
                    info[file_name_key] = file_name
                else:
                    info[key_name] = cell.value
            info_array.append(info)
            log_print(LogType.SUCCESS, f"{person_name}님의 데이터를 저장했습니다.")
            row_idx += 1
        return info_array
    except Exception as e:
        person_name, property = e.args
        log_print(
            LogType.ERROR,
            f"{person_name}님의 {property}에 해당하는 정보가 없는 것 같습니다. 엑셀 파일을 확인해주세요.",
        )
        sys.exit(0)


if __name__ == "__main__":
    pass
