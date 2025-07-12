import os
import time
from index import trim_movie, download_movie
from uploader import upload_clip

import requests

try:
    ip = requests.get("https://api.ipify.org").text
    print(f"🌍 Public IP of Railway container: {ip}")
except Exception as e:
    print("❌ Failed to fetch public IP:", e)


MOVIE_PATH = "test.mkv"

# ✅ Force re-download of new test video
if os.path.exists(MOVIE_PATH):
    os.remove(MOVIE_PATH)

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
