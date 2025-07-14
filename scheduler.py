import os
import time
from index import trim_movie, download_movie
from uploader import upload_clip

MOVIE_PATH = "test.mkv"

if __name__ == "__main__":
    while True:
        print("\n⏰ Starting Instagram automation cycle...\n")

        try:
            # 1. Download movie if not found
            if not os.path.exists(MOVIE_PATH):
                print("🎥 Movie not found. Downloading...")
                download_movie()
                print("✅ Download complete.")

            # 2. Trim clips if not already present
            if not os.path.exists("clips") or not os.listdir("clips"):
                print("✂️ No clips found. Trimming movie...")
                trim_movie()
                print("✅ Trimming done.")

            # 3. Upload one clip
            print("⬆️ Uploading a clip...")
            upload_clip()
            print("✅ Upload complete.")

        except Exception as e:
            print(f"⚠️ Error during cycle: {e}")

        print("🕒 Sleeping for 1 minute...\n")
        time.sleep(3*60*60)
