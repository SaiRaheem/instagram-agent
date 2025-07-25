import os
import gdown
import logging
from moviepy.editor import VideoFileClip
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
MOVIE_URL = os.getenv("MOVIE_URL")
MOVIE_PATH = os.getenv("MOVIE_PATH", "test.mkv")
CLIPS_DIR = os.getenv("CLIPS_DIR", "clips")
CLIP_DURATION = int(os.getenv("CLIP_DURATION", "60"))  # seconds
MAX_CLIPS = int(os.getenv("MAX_CLIPS", "1"))  # testing limit
VIDEO_CODEC = os.getenv("VIDEO_CODEC", "libx264")
AUDIO_CODEC = os.getenv("AUDIO_CODEC", "aac")

def download_movie(url=None, dest=None):
    try:
        url = url or MOVIE_URL
        dest = dest or MOVIE_PATH
        
        if not url:
            raise ValueError("No movie URL provided")
            
        logger.info(f"Downloading movie from {url}...")
        gdown.download(url, dest, quiet=False)
        logger.info(f"Download complete: {dest}")
    except Exception as e:
        logger.error(f"Download failed: {str(e)}")
        raise

def trim_movie(movie_path=None, output_folder=None, clip_length=None, max_clips=None):
    try:
        movie_path = movie_path or MOVIE_PATH
        output_folder = output_folder or CLIPS_DIR
        clip_length = clip_length or CLIP_DURATION
        max_clips = max_clips or MAX_CLIPS

        logger.info(f"Trimming {movie_path} into clips...")
        os.makedirs(output_folder, exist_ok=True)

        clip = VideoFileClip(movie_path)
        duration = int(clip.duration)
        count = 0

        for start in range(0, duration, clip_length):
            if count >= max_clips:
                break
                
            end = min(start + clip_length, duration)
            output_path = os.path.join(output_folder, f"clip_{count:04d}.mp4")
            
            logger.info(f"Creating clip {count+1}: {output_path} ({start}s-{end}s)")
            
            subclip = clip.subclip(start, end)
            subclip.write_videofile(
                output_path,
                codec=VIDEO_CODEC,
                audio_codec=AUDIO_CODEC,
                preset="slow",
                ffmpeg_params=[
                    "-crf", "18",
                    "-movflags", "+faststart",
                    "-pix_fmt", "yuv420p"
                ],
                threads=4,
                logger=None
            )
            count += 1

        logger.info(f"Created {count} clips in {output_folder}")
        clip.close()
    except Exception as e:
        logger.error(f"Trimming failed: {str(e)}")
        raise

def cleanup_resources():
    try:
        # Remove movie file if exists
        if os.path.exists(MOVIE_PATH):
            os.remove(MOVIE_PATH)
            logger.info(f"Removed movie file: {MOVIE_PATH}")
            
        # Optionally remove clips directory
        # if os.path.exists(CLIPS_DIR):
        #     shutil.rmtree(CLIPS_DIR)
        #     logger.info(f"Removed clips directory: {CLIPS_DIR}")
    except Exception as e:
        logger.error(f"Cleanup failed: {str(e)}")

if __name__ == "__main__":
    try:
        if not os.path.exists(MOVIE_PATH):
            download_movie()
        trim_movie()
    except Exception as e:
        logger.critical(f"Error in main execution: {str(e)}")