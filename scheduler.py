import os
import time
from index import trim_movie, download_movie
from uploader import upload_clip

MOVIE_URL = "https://drive.google.com/file/d/1jP_09FYxyb1QZhzwWzglHRWS8ZaRZnso/view?usp=drive_link"
MOVIE_FILENAME = "500.mkv"

def ensure_movie():
    if not os.path.exists(MOVIE_FILENAME):
        print("🎥 Movie not found locally. Downloading...")
        download_movie(MOVIE_URL, MOVIE_FILENAME)
    else:
        print("✅ Movie already exists locally.")

def ensure_clips():
    if not os.path.exists("clips") or not os.listdir("clips"):
        print("✂️ No clips found. Trimming movie...")
        trim_movie(MOVIE_FILENAME)
    else:
        print("✅ Clips already available.")

if __name__ == "__main__":
    while True:
        print("⏰ Starting Instagram automation cycle...")
        try:
            ensure_movie()
            ensure_clips()
            upload_clip()
        except Exception as e:
            print(f"⚠️ Error during cycle: {e}")
        print("🕒 Sleeping for 4 hours...")
        time.sleep(4 * 60 * 60)
