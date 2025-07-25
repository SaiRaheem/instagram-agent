import os
import time
import logging
from datetime import datetime
from dotenv import load_dotenv
from index import trim_movie, download_movie, cleanup_resources
from uploader import upload_clip

# Load environment variables
load_dotenv()

# Configuration
MOVIE_PATH = os.getenv("MOVIE_PATH", "test.mkv")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))  # seconds
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('scheduler.log')
    ]
)

logger = logging.getLogger(__name__)

def main_cycle():
    retry_count = 0
    while retry_count < MAX_RETRIES:
        try:
            logger.info("Starting automation cycle...")

            # 1. Download movie if not found
            if not os.path.exists(MOVIE_PATH):
                logger.info("Movie not found. Downloading...")
                download_movie()
                logger.info("Download complete.")

            # 2. Trim clips if not already present
            clips_dir = os.getenv("CLIPS_DIR", "clips")
            if not os.path.exists(clips_dir) or not os.listdir(clips_dir):
                logger.info("No clips found. Trimming movie...")
                trim_movie()
                logger.info("Trimming complete.")

            # 3. Upload one clip
            logger.info("Attempting to upload clip...")
            success = upload_clip()
            if success:
                logger.info("Upload completed successfully.")
                cleanup_resources()  # Cleanup after successful upload
                return True
            else:
                logger.warning("Upload skipped or failed.")
                return False

        except Exception as e:
            logger.error(f"Error during cycle (attempt {retry_count + 1}/{MAX_RETRIES}): {str(e)}")
            retry_count += 1
            time.sleep(10)  # Short delay before retry

    logger.error("Max retries reached. Ending cycle.")
    return False

if __name__ == "__main__":
    logger.info("🚀 Starting Instagram automation scheduler")
    try:
        while True:
            main_cycle()
            logger.info(f"Sleeping for {CHECK_INTERVAL} seconds...")
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        logger.info("Shutting down scheduler...")
    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}")
    finally:
        cleanup_resources()