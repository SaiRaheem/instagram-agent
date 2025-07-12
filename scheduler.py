import os
import time
from index import trim_movie, download_movie
from uploader import upload_clip

MOVIE_PATH = "500.mkv"

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
                trim_movie()
                print("✅ Trimming done.")

            print("⬆️ Uploading a clip...")
            upload_clip()
            print("✅ Upload complete.")

        except Exception as e:
            print(f"⚠️ Error during cycle: {e}")

        print("🕒 Sleeping for 1 minute...")
        time.sleep(60)
