import os
import datetime
from typing import List
import openpyxl as xl
import openpyxl.worksheet.worksheet as worksheet
from .configs import ExcelSheetCfg
from .error import CustomException
from .logger import Logger


class ExcelFile:
    def __init__(self, file_path: str) -> None:
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
