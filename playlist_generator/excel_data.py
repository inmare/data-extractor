import os
import datetime
from typing import List
import openpyxl as xl
import openpyxl.worksheet.worksheet as worksheet
from .configs import get_data_by_key_name, ExcelDataCfg, ExcelSheetCfg, DataEnum
from .error import CustomException
from .logger import Logger


def _get_name_from_row(sheet: xl.Workbook.worksheets, row_idx: int):
    col_idx = 1
    value = sheet.cell(row=ExcelSheetCfg.KeyDataRow.value, column=col_idx).value
    while value is not None:
        # 데이터 시트의 부원 이름에 해당하는 부분은 무조건 적어둘 거라는 가정하에 작성
        if value == ExcelDataCfg.Name.keyname:
            return sheet.cell(row=row_idx, column=col_idx).value
        col_idx += 1
        value = sheet.cell(row=ExcelSheetCfg.KeyDataRow.value, column=col_idx).value
    raise CustomException(
        "해당 열에서 이름에 해당하는 항목을 찾을 수 없습니다. 이러면 안되는데..."
    )


def _process_nickname():
    nickname_char = ord("A")
    while True:
        yield f"익명{chr(nickname_char)}"
        nickname_char += 1


class ExcelData:
    __process_func = {
        ExcelDataCfg.Nickname: lambda nickname: (
            next(_process_nickname()) if nickname is None else nickname
        ),
        ExcelDataCfg.OriginalLink: lambda link: None if link is None else link,
        ExcelDataCfg.KorLyricsLink: lambda link: None if link is None else link,
    }

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_data_order(sheet: worksheet) -> List[DataEnum]:
        """
        엑셀에서 존재해야 하는 데이터들이 어떤 순서대로 정렬되어 있는지 반환하는 함수

        Args:
            sheet (worksheet): 엑셀 시트

        Returns:
            List[ExcelData]: 엑셀 시트의 순서대로 정렬된 데이터의 종류들
        """
        try:
            # 특정 key 값이 어떤 열에 존재하는지 확인하고, 해당 순서를 list로 만들기
            key_row_idx = ExcelSheetCfg.KeyDataRow.value
            ordered_data = []  # 정렬된 데이터를 저장할 배열

            col_idx = 1
            while sheet.cell(row=key_row_idx, column=col_idx).value is not None:
                # 열을 한 칸씩 띄우면서 데이터를 작성하는 미친 사람이 없다는 가정하에 작성
                key_name = sheet.cell(row=key_row_idx, column=col_idx).value
                data = get_data_by_key_name(ExcelDataCfg, key_name)
                if data is None:
                    raise CustomException(
                        f"찾으려고 하는 {key_name}이 엑셀 시트에는 없습니다."
                    )
                ordered_data.append(data)
                col_idx += 1

            return ordered_data
        except Exception as e:
            if isinstance(e, CustomException):
                raise e
            else:
                raise Exception(
                    f"예상치 못한 에러가 발생하였습니다. 아래는 발생한 에러메세지 입니다.\n{e}"
                )

    @staticmethod
    def get_data(sheet: worksheet, ordered_data: List[ExcelDataCfg]) -> List[dict]:
        """
        엑셀 파일에서 데이터를 가져오는 함수

        Args:
            sheet (worksheet): 엑셀 시트
            ordered_data (List[ExcelData]): 엑셀 시트의 순서대로 정렬된 데이터의 종류들
        """
        row_idx = ExcelSheetCfg.StartDataRow.value

        playlist_data = []

        # 이름이 더 이상 없을 때까지 열을 하나씩 내려가면서 데이터 추출
        while sheet.cell(row=row_idx, column=1).value is not None:
            data_dict = {}

            person_name = _get_name_from_row(sheet, row_idx)
            for idx, data in enumerate(ordered_data):
                value = sheet.cell(row=row_idx, column=idx + 1).value
                # 해당 데이터가 꼭 있어야 하는 데이터인지 확인
                if data.essential and value is None:
                    # 만약 없다면 에러 발생
                    raise CustomException(
                        f"{person_name}의 {data.ui_name}에 해당하는 정보가 없는 것 같습니다. 엑셀 파일을 확인해주세요."
                    )
                # 데이터가 있다면 데이터의 종류에 따라서 데이터 가공
                if data in ExcelData.__process_func:
                    processed_value = ExcelData.__process_func[data](value)
                    data_dict[data.keyname] = processed_value
                else:
                    data_dict[data.keyname] = value

            playlist_data.append(data_dict)
            Logger.info(f"{person_name}의 정보를 저장했습니다.")
            row_idx += 1

        return playlist_data


class ExcelFile:
    def __init__(self, file_path: os.path) -> None:
        self.path = file_path
        self.date = None
        self.data_sheet = None

        try:
            Logger.debug(f"{file_path}를 읽는 중입니다...")
            sheets = self._get_sheets()
            date_sheet = sheets[ExcelSheetCfg.DateSheetIdx.value]
            recommend_sheet = sheets[ExcelSheetCfg.RecommendSheetIdx.value]
            self.date = self._get_date(date_sheet)
            self.data_sheet = recommend_sheet
            Logger.info(f"{file_path}를 읽어오는데 성공했습니다.")
        except Exception as e:
            raise e

    def _get_sheets(self) -> xl.Workbook.worksheets:
        try:
            workbook = xl.load_workbook(self.path)
            return workbook.worksheets
        except Exception as e:
            raise e

    def _get_date(self, sheet: worksheet) -> datetime.date:
        try:
            year_cell = ExcelSheetCfg.YearCell.value
            month_cell = ExcelSheetCfg.MonthCell.value
            year = sheet[year_cell].value
            month = sheet[month_cell].value
            if year_cell is None or month_cell is None:
                raise CustomException(
                    f"엑셀 파일 {self.path}의 날짜 셀이 비어있습니다. {year_cell}셀에는 연도, {month_cell}셀에는 월을 입력한 다음 다시 시도해주세요."
                )
            # 만약 2자리 수만 연도로 입력할 경우 2000년대로 간주
            if year < 100:
                year += 2000
            return datetime.date(year=int(year), month=int(month), day=1)
        except Exception as e:
            raise e


# def get_sheets(excel_file_name: str):
#     if excel_file_name[-5:] != ".xlsx":
#         excel_path = f"{excel_file_name}.xlsx"
#     else:
#         excel_path = excel_file_name
#     try:
#         workbook = xl.load_workbook(excel_path)
#         sheets = workbook.worksheets
#         date_sheet = sheets[0]
#         recommend_sheet = sheets[1]

#         return [date_sheet, recommend_sheet]
#     except Exception as _:
#         raise Exception(
#             f"파일 {excel_file_name}을 열지 못했습니다. 해당 파일이 정확한 형식의 파일인지 확인한 다음 다시 시도해주세요."
#         )


# def get_date(sheet):
#     year_cell = config.DATE_CELL["year"]
#     month_cell = config.DATE_CELL["month"]

#     try:
#         year = int(sheet[year_cell].value)
#         month = int(sheet[month_cell].value)
#         date = datetime.date(year, month, 1)
#         log_print(
#             LogType.SUCCESS, f"{date.year}년 {date.month}월 플레이리스트를 생성합니다."
#         )
#         return date
#     except Exception as e:
#         log_print(LogType.ERROR, f"데이터를 가져오는데 실패했습니다.")
#         log_print(LogType.ERROR, e)
#         log_print(
#             LogType.ERROR,
#             f"추천하는 법 시트의 {year_cell}셀과 {month_cell}셀에 년도와 월이 제대로 기입되어 있는지 확인해주세요.",
#         )
#         input("Enter키를 누르면 프로그램이 종료 됩니다...")


# def create_file_name(song_name_kor):
#     file_name = song_name_kor
#     replace_str = '\\/:*?"<>|'
#     for char in replace_str:
#         file_name = file_name.replace(char, "_")
#     return file_name


# def get_info(sheet):
#     log_print(LogType.PROGRESS, f"엑셀 파일에서 데이터를 가져오는 중입니다...")

#     info_array = []
#     anon_idx = ord("A")
#     file_name_key = config.ADDITIONAL_KEY["파일 이름"]  # 파일 이름에 해당하는 키 이름

#     row_idx = config.START_ROW

#     try:
#         # 다운 가능한 링크가 유튜브가 아닌 정보를 저장
#         warned_info = []
#         while sheet.cell(row=row_idx, column=1).value is not None:
#             info = {}
#             person_name = None
#             is_warned = False  # 다운가능한 링크가 이상한지
#             for idx, key in enumerate(config.EXCEL_KEY.items()):
#                 cell = sheet.cell(row=row_idx, column=idx + 1)
#                 prop = key[0]
#                 key_name = key[1]
#                 if prop == "이름":
#                     person_name = cell.value

#                 # 필요한 데이터 부분에 이름이 없을 경우 에러 발생
#                 if prop in config.ESSENTIAL_KEY and cell.value is None:
#                     raise CellValueError(person_name, prop)

#                 # 닉네임이 없을 경우 익명으로 처리
#                 if prop == "닉네임" and cell.value is None:
#                     info[key_name] = "익명" + chr(anon_idx)
#                     anon_idx += 1
#                 # 파일명에 사용할 수 없는 문자 변경
#                 elif prop == "한국어 노래 제목":
#                     file_name = create_file_name(cell.value)
#                     info[key_name] = cell.value
#                     info[file_name_key] = file_name
#                 # 원본 링크가 링크의 형식이 아닐 경우 value를 None으로 처리
#                 elif prop == "원본 링크":
#                     if cell.value is None:
#                         info[key_name] = None
#                         continue
#                     is_valid_link = cell.value.startswith("http")
#                     info[key_name] = cell.value if is_valid_link else None
#                 # 다운로드 가능 링크가 youtube의 링크 형식이 아닐 경우 경고문 출력
#                 elif prop == "다운로드 가능 링크":
#                     yt_link_regex = re.compile(
#                         r"^http?s:\/\/(www\.youtube\.com\/watch\?v=|youtu\.be\/)[A-Za-z0-9-_]{11}.*$"
#                     )
#                     is_valid_link = yt_link_regex.match(cell.value)
#                     if not is_valid_link:
#                         is_warned = True
#                     info[key_name] = cell.value
#                 else:
#                     info[key_name] = cell.value
#             info_array.append(info)
#             if is_warned:
#                 warned_info.append(info)
#             log_print(LogType.SUCCESS, f"{person_name}님의 데이터를 저장했습니다.")
#             row_idx += 1

#         # 만약 유튜브링크가 아닌 링크가 있다면 사용자에게 알림
#         if warned_info:
#             log_print(
#                 LogType.WARNING,
#                 f"일부 다운로드 가능한 링크가 유튜브 링크가 아닌 것 같습니다.",
#             )
#             for info in warned_info:
#                 log_print(
#                     LogType.WARNING,
#                     f"{info[config.EXCEL_KEY['이름']]}-{info[config.EXCEL_KEY['다운로드 가능 링크']]}",
#                 )

#             user_answer = None

#             while user_answer not in ["yes", "no"]:
#                 user_answer = input(
#                     "다운로드를 계속 진행하려면 yes, 중단하려면 no을 입력하고 Enter를 눌러주세요: "
#                 )
#                 if user_answer == "no":
#                     raise UserInvokedError("사용자가 프로그램을 중단했습니다.")
#                 elif user_answer == "yes":
#                     log_print(LogType.PROGRESS, "다운로드를 계속 진행합니다.")
#                     break

#         return info_array
#     except Exception as _:
#         raise


if __name__ == "__main__":
    pass
