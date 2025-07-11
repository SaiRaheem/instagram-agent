import os
import time
from index import trim_movie, download_movie
from uploader import upload_clip

MOVIE_PATH = "500.mkv"
DOWNLOAD_URL = "https://drive.google.com/uc?export=download&id=1jP_09FYxyb1QZhzwWzglHRWS8ZaRZnso"

if __name__ == "__main__":
    while True:
        print("⏰ Starting Instagram automation cycle...")

        try:
            if not os.path.exists(MOVIE_PATH):
                print("🎥 Movie not found locally. Downloading...")
                download_movie()
                print("✅ Download complete.")

            if not os.path.exists("clips") or not os.listdir("clips"):
                print("✂️ No clips found. Trimming movie...")
                trim_movie(MOVIE_PATH)
                print("✅ Trimming done.")

            print("⬆️ Uploading a clip...")
            upload_clip()
            print("✅ Upload complete.")

        except Exception as e:
            print(f"⚠️ Error during cycle: {e}")

        print("🕒 Sleeping for 1 minute...")
        time.sleep(60)  # 1 minute
