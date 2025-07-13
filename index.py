import os
import gdown
from moviepy.editor import VideoFileClip

# === CONFIG ===
MOVIE_URL = "https://drive.google.com/uc?id=1z7YRfanuXCGmwnh1hKKc7bG1n9zoh2sF"
MOVIE_PATH = "test.mkv"
CLIPS_DIR = "clips"
CLIP_DURATION = 15  # seconds
MAX_CLIPS = 5       # testing limit

def download_movie(url=MOVIE_URL, dest=MOVIE_PATH):
    print("⬇️ Downloading movie...")
    gdown.download(url, dest, quiet=False)
    print("✅ Download complete.")

def trim_movie(movie_path=MOVIE_PATH, output_folder=CLIPS_DIR, clip_length=CLIP_DURATION, max_clips=MAX_CLIPS):
    print("✂️ Trimming into clips...")
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

        print(f"🎬 Saving: {output_path}")
        subclip.write_videofile(
            output_path,
            codec="libx264",
            audio=True,
            logger=None,
            ffmpeg_params=["-preset", "ultrafast", "-crf", "32", "-vf", "scale=640:-1"]
        )
        count += 1

    print(f"✅ Done. {count} clips created.")

if __name__ == "__main__":
    if not os.path.exists(MOVIE_PATH):
        download_movie()
    trim_movie()
