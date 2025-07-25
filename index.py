import os
import gdown
from moviepy.editor import VideoFileClip

MOVIE_URL = os.getenv("MOVIE_URL")
MOVIE_PATH = "video.mp4"  # Using MP4 avoids conversion issues
CLIPS_DIR = "clips"
CLIP_DURATION = 60  # seconds

def download_movie():
    if not os.path.exists(MOVIE_PATH):
        gdown.download(MOVIE_URL, MOVIE_PATH, quiet=False)

def trim_movie():
    os.makedirs(CLIPS_DIR, exist_ok=True)
    clip = VideoFileClip(MOVIE_PATH)
    
    for i, start in enumerate(range(0, int(clip.duration), CLIP_DURATION)):
        end = min(start + CLIP_DURATION, clip.duration)
        clip.subclip(start, end).write_videofile(
            f"{CLIPS_DIR}/clip_{i:04d}.mp4",
            codec="libx264",
            audio_codec="aac",
            threads=2,
            logger=None
        )
    clip.close()

if __name__ == "__main__":
    download_movie()
    trim_movie()