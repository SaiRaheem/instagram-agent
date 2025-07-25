import os
import time
import logging
import requests
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Cloudinary configuration
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Instagram API configuration
INSTAGRAM_API_VERSION = os.getenv("INSTAGRAM_API_VERSION", "v19.0")
MAX_PUBLISH_WAIT = int(os.getenv("MAX_PUBLISH_WAIT", "300"))  # 5 minutes
PUBLISH_CHECK_INTERVAL = int(os.getenv("PUBLISH_CHECK_INTERVAL", "30"))  # seconds

def upload_to_cloudinary(file_path):
    try:
        logger.info(f"Uploading {file_path} to Cloudinary...")
        result = cloudinary.uploader.upload_large(
            file_path,
            resource_type="video",
            chunk_size=6000000,  # 6MB chunks
            timeout=300
        )
        logger.info(f"Cloudinary upload successful: {result['secure_url']}")
        return result["secure_url"]
    except Exception as e:
        logger.error(f"Cloudinary upload failed: {str(e)}")
        return None

def check_container_status(container_id):
    try:
        response = requests.get(
            f"https://graph.facebook.com/{INSTAGRAM_API_VERSION}/{container_id}",
            params={
                "fields": "status_code",
                "access_token": os.getenv("IG_TOKEN")
            }
        )
        data = response.json()
        return data.get("status_code") == "FINISHED"
    except Exception as e:
        logger.error(f"Error checking container status: {str(e)}")
        return False

def upload_clip():
    try:
        posted_file = os.getenv("POSTED_FILE", "posted.txt")
        clips_dir = os.getenv("CLIPS_DIR", "clips")

        # Read posted history
        posted = set()
        if os.path.exists(posted_file):
            with open(posted_file, "r", encoding="utf-8") as f:
                posted = set(f.read().splitlines())

        # Find next clip
        clips = sorted(
            f for f in os.listdir(clips_dir) 
            if f.endswith((".mp4", ".mov", ".avi"))
        )
        next_clip = next((clip for clip in clips if clip not in posted), None)
        
        if not next_clip:
            logger.info("All clips have been uploaded.")
            return False

        clip_path = os.path.join(clips_dir, next_clip)

        # 1. Upload to Cloudinary
        clip_url = upload_to_cloudinary(clip_path)
        if not clip_url:
            return False

        logger.info(f"Preparing to upload {next_clip} to Instagram...")

        # 2. Create media container
        container_response = requests.post(
            f"https://graph.facebook.com/{INSTAGRAM_API_VERSION}/{os.getenv('IG_USER_ID')}/media",
            params={
                "media_type": "REELS",
                "video_url": clip_url,
                "caption": os.getenv("IG_CAPTION", "📽️ Auto-uploaded Reel"),
                "access_token": os.getenv("IG_TOKEN")
            },
            timeout=30
        )

        if container_response.status_code != 200:
            logger.error(f"Container creation failed: {container_response.text}")
            return False

        container = container_response.json()
        logger.info(f"Container created: {container}")

        if "id" not in container:
            logger.error("No container ID in response")
            return False

        # 3. Wait for container to be ready
        container_id = container["id"]
        logger.info("Waiting for container to be ready...")
        
        start_time = time.time()
        while time.time() - start_time < MAX_PUBLISH_WAIT:
            if check_container_status(container_id):
                break
            time.sleep(PUBLISH_CHECK_INTERVAL)
        else:
            logger.error("Container not ready within timeout period")
            return False

        # 4. Publish media
        publish_response = requests.post(
            f"https://graph.facebook.com/{INSTAGRAM_API_VERSION}/{os.getenv('IG_USER_ID')}/media_publish",
            params={
                "creation_id": container_id,
                "access_token": os.getenv("IG_TOKEN")
            },
            timeout=30
        )

        if publish_response.status_code != 200:
            logger.error(f"Publish failed: {publish_response.text}")
            return False

        logger.info(f"Publish successful: {publish_response.json()}")

        # 5. Mark clip as posted
        with open(posted_file, "a") as f:
            f.write(f"{next_clip}\n")

        return True

    except Exception as e:
        logger.error(f"Error in upload_clip: {str(e)}")
        return False