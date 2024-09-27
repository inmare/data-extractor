from playlist_generator import playlist
from playlist_generator.project_config import (
    FFMPEG_PATH,
    MUSIC_YDL_OPTS,
    THUMBNAIL_YDL_OPTS,
)
import sys
import os

program_dir = os.path.dirname(sys.argv[0])
file_name = sys.argv[1]
MUSIC_YDL_OPTS["ffmpeg_location"] = program_dir + FFMPEG_PATH
THUMBNAIL_YDL_OPTS["ffmpeg_location"] = program_dir + FFMPEG_PATH

playlist.generate(str(program_dir), file_name)
