import time
from uploader import upload_clip

if __name__ == "__main__":
    while True:
        print("⏰ Uploading next clip...")
        try:
            upload_clip()
        except Exception as e:
            print(f"⚠️ Error during upload: {e}")
        print("🕒 Sleeping for 4 hours...")
        time.sleep(4 * 60 * 60)
  