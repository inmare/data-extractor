import os
import json
import shutil
import zipfile
import datetime
from typing import List
from .configs import PathCfg


def delete_folder(program_dir: str, folder: PathCfg):
    """
    특정 폴더를 삭제하는 함수

    Args:
        program_dir (str): 현재 프로그램이 실행되는 디렉터리
        folder (PathCfg): 삭제할 폴더
    """

    folder_path = os.path.join(program_dir, folder.value)

    try:
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
    except Exception as e:
        raise e


def delete_file(program_dir: str, file_name: str):
    """
    특정 파일을 삭제하는 함수

    Args:
        program_dir (str): 현재 프로그램이 실행되는 디렉터리
        file_name (str): 삭제할 파일 이름
    """

    file_path = os.path.join(program_dir, file_name)

    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        raise e


def create_folder(program_dir: str, folder: PathCfg):
    """
    특정 폴더를 생성하는 함수
    이때 해당 폴더가 이미 존재하면 삭제 후 다시 생성

    Args:
        program_dir (str): 현재 프로그램이 실행되는 디렉터리
        folder (PathCfg): 생성할 폴더
    """

    folder_path = os.path.join(program_dir, folder.value)

    try:
        delete_folder(program_dir, folder)
        os.makedirs(folder_path)
    except Exception as e:
        raise e


def get_file_prefix(date: datetime, created_time: datetime) -> str:
    """
    파일을 생성할 때 사용될 이름을 반환하는 함수

    Args:
        date (datetime): 플레이리스트의 날짜
        created_time (datetime): 플레이리스트 생성 시간

    Returns:
        str: 파일 이름의 접두사. 해당 이름에 .json이나 .zip 등을 붙여서 사용
    """
    return f"{date.strftime('%Y년 %m월')} 플레이리스트 정보 {created_time}"


def save_json_file(program_dir: str, file_name: str, data: dict):
    """
    json 파일을 작성하는 함수

    Args:
        program_dir (str): 현재 프로그램이 실행되는 디렉터리
        file_name (str): 파일 이름
        data (dict): json 파일에 작성할 데이터
    """

    file_path = os.path.join(program_dir, file_name)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        raise e


def save_zip_file(
    program_dir: str,
    file_name: str,
    original_path: List[str],
    save_path: List[str],
):
    """
    주어진 파일의 원래 경로들과 저장할 경로들을 이용하여 zip 파일을 생성하는 함수

    Args:
        program_dir (str): 현재 프로그램이 실행되는 디렉터리
        file_name (str): 파일 이름
        original_path (List[str]): 원래 파일 경로들
        save_path (List[str]): 저장할 파일 경로들
    """
    file_path = os.path.join(program_dir, file_name)
    try:
        zipf = zipfile.ZipFile(file_path, "w", zipfile.ZIP_DEFLATED)

        for original, save in zip(original_path, save_path):
            zipf.write(original, save)
        zipf.close()
    except Exception as e:
        raise e
