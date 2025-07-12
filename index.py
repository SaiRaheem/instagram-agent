import os
import gdown
from moviepy.editor import VideoFileClip

# Constants
MOVIE_URL = "https://drive.google.com/uc?id=1jP_09FYxyb1QZhzwWzglHRWS8ZaRZnso"
MOVIE_PATH = "500.mkv"
CLIPS_DIR = "clips"
CLIP_DURATION = 60
MAX_CLIPS = 5

def download_movie(url=MOVIE_URL, dest=MOVIE_PATH):
    print("⬇️ Downloading movie from Google Drive with gdown...")
    gdown.download(url, dest, quiet=False)
    print("✅ Movie downloaded successfully.")

def trim_movie(movie_path=MOVIE_PATH, output_folder=CLIPS_DIR, clip_length=CLIP_DURATION, max_clips=MAX_CLIPS):
    print("✂️ Trimming movie into clips...")
    os.makedirs(output_folder, exist_ok=True)
    clip = VideoFileClip(movie_path)
    duration = int(clip.duration)
    count = 0

    for start in range(0, duration, clip_length):
        if count >= max_clips:
            break
        end = min(start + clip_length, duration)
        subclip = clip.subclip(start, end)
        output_path = os.path.join(output_folder, f"clip_{count:04d}.mp4")
        print(f"🎬 Saving clip {count + 1}: {output_path}")
        subclip.write_videofile(output_path, codec='libx264', audio=False, logger=None)
        count += 1

    print(f"✅ Created {count} clips.")

if __name__ == "__main__":
    if not os.path.exists(MOVIE_PATH):
        download_movie()
    trim_movie()
