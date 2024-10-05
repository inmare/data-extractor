import PyInstaller.__main__
import zipfile
import os

current_dir = os.chdir()
zip_file_name = "Playlist-Downloader.zip"
zip_file_path = os.path.join(current_dir, zip_file_name)

if os.path.exists(zip_file_path):
    os.remove(zip_file_path)

PyInstaller.__main__.run(["main.py", "--onefile", "--icon", "icon.ico"])

zipf = zipfile.ZipFile(
    zip_file_path,
    "w",
    zipfile.ZIP_DEFLATED,
)
zipf.write(
    os.path.join(current_dir, "dist", "main.exe"),
    os.path.join("플레이리스트 다운로더.exe"),
)
zipf.write(
    os.path.join(current_dir, "assets", "ffmpeg.exe"),
    os.path.join("assets", "ffmpeg.exe"),
)
zipf.write(
    os.path.join(current_dir, "assets", "ffprobe.exe"),
    os.path.join("assets", "ffprobe.exe"),
)
zipf.close()
