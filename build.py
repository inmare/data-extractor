import PyInstaller.__main__
import zipfile
import os

if os.path.exists("Playlist-Downloader.zip"):
    os.remove("Playlist-Downloader.zip")

PyInstaller.__main__.run(["main.py", "--onefile", "--icon", "icon.ico"])

zipf = zipfile.ZipFile(
    "Playlist-Downloader.zip",
    "w",
    zipfile.ZIP_DEFLATED,
)
zipf.write("dist/main.exe", "플레이리스트 다운로더.exe")
zipf.write("ffmpeg/ffmpeg.exe", "ffmpeg/ffmpeg.exe")
zipf.close()
