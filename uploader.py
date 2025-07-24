import os
import time
import requests
import cloudinary
import cloudinary.uploader

# === TEMPORARY HARDCODED CREDENTIALS (for testing only) ===
cloudinary.config(
    cloud_name="your_cloud_name",
    api_key="your_api_key",
    api_secret="your_api_secret"
)

# === Instagram credentials ===
ACCESS_TOKEN = os.getenv("IG_TOKEN")
IG_USER_ID = os.getenv("IG_USER_ID")

def upload_to_cloudinary(file_path):
    try:
        print(f"☁️ Uploading {file_path} to Cloudinary...")
        result = cloudinary.uploader.upload_large(file_path, resource_type="video")
        print(f"✅ Cloudinary upload: {result['secure_url']}")
        return result["secure_url"]
    except Exception as e:
        print(f"❌ Cloudinary upload failed: {e}")
        return None

def upload_clip():
    posted_file = "posted.txt"
    clips_dir = "clips"

    # Read posted history
    posted = set()
    if os.path.exists(posted_file):
        with open(posted_file, "r", encoding="utf-8", errors="ignore") as f:
            posted = set(f.read().splitlines())

    # Find next clip
    clips = sorted(f for f in os.listdir(clips_dir) if f.endswith(".mp4"))
    next_clip = next((clip for clip in clips if clip not in posted), None)
    if not next_clip:
        print("🎉 All clips uploaded.")
        return False

    clip_path = os.path.join(clips_dir, next_clip)

    # 1. Upload to Cloudinary
    clip_url = upload_to_cloudinary(clip_path)
    if not clip_url:
        return False

    print(f"📤 Uploading {next_clip} to Instagram from {clip_url}")

    # 2. Create media container (REEL)
    container_res = requests.post(
        f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media",
        params={
            "media_type": "REELS",
            "video_url": clip_url,
            "caption": "📽️ Auto-uploaded Reel",
            "access_token": ACCESS_TOKEN
        }
    )
    container = container_res.json()
    print("📦 Container Response:", container)

    if "id" not in container:
        print("❌ Failed to create media container.")
        return False

    # 3. Publish media after short delay
    print("⏳ Waiting 2 minutes before publishing...")
    time.sleep(2 * 60)

    publish_res = requests.post(
        f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish",
        params={
            "creation_id": container["id"],
            "access_token": ACCESS_TOKEN
        }
    )
    print("✅ Published Response:", publish_res.json())

    # 4. Mark clip as posted
    with open(posted_file, "a") as f:
        f.write(f"{next_clip}\n")

    return True
