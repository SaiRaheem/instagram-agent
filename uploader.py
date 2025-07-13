import os
import requests
import time
import cloudinary
import cloudinary.uploader

# Load credentials
ACCESS_TOKEN = os.getenv("IG_TOKEN")
IG_USER_ID = os.getenv("IG_USER_ID")

# Setup Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

print("🔍 DEBUG CLOUDINARY CONFIG")
print("cloud_name:", os.getenv("CLOUDINARY_CLOUD_NAME"))
print("api_key:", os.getenv("CLOUDINARY_API_KEY"))
print("api_secret exists:", bool(os.getenv("CLOUDINARY_API_SECRET")))

def upload_to_cloudinary(file_path):
    try:
        print(f"☁️ Uploading {file_path} to Cloudinary...")
        result = cloudinary.uploader.upload_large(file_path, resource_type="video")
        print(f"✅ Cloudinary upload done: {result['secure_url']}")
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
        return

    clip_path = os.path.join(clips_dir, next_clip)

    # 1️⃣ Upload to Cloudinary
    clip_url = upload_to_cloudinary(clip_path)
    if not clip_url:
        return

    print(f"📤 Uploading {next_clip} to Instagram from {clip_url}")

    # 2️⃣ Create media container
    container_res = requests.post(
        f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media",
        params={
            "media_type": "REEL",
            "video_url": clip_url,
            "caption": f"🔥 Auto-posted: {next_clip}",
            "access_token": ACCESS_TOKEN
        }
    )
    container = container_res.json()
    print("📦 Container Response:", container)

    if "id" not in container:
        print("❌ Failed to create media container:", container)
        return

    # 3️⃣ Wait briefly before publishing
    time.sleep(5)

    publish_res = requests.post(
        f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish",
        params={
            "creation_id": container["id"],
            "access_token": ACCESS_TOKEN
        }
    )
    print("✅ Published Response:", publish_res.json())

    # 4️⃣ Mark as posted
    with open(posted_file, "a") as f:
        f.write(f"{next_clip}\n")
