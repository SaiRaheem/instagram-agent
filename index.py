import os
import gdown
from moviepy.editor import VideoFileClip

# === CONFIG ===
MOVIE_URL = "https://drive.google.com/uc?id=1kuTuAhJV3DxpufNi0riijj8ub0q2FDkt"
MOVIE_PATH = "test.mkv"
CLIPS_DIR = "clips"
CLIP_DURATION = 30  # seconds
MAX_CLIPS = 1       # testing limit

# === FFmpeg Filter String (no scale, max quality) ===
FILTERS = (
    "transpose=1,"
    "eq=brightness=0.1:contrast=1.4:saturation=1.4,"
    "unsharp=5:5:1.0:5:5:0.0,"
    "curves=preset=medium_contrast"
)

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
            logger='bar',
            ffmpeg_params=[
                "-preset", "slow",
                "-crf", "20",
                "-movflags", "+faststart",
                "-pix_fmt", "yuv420p",
                "-vf", FILTERS
            ]
        )
        count += 1

    print(f"✅ Done. {count} clips created.")


if __name__ == "__main__":
    if not os.path.exists(MOVIE_PATH):
        download_movie()
    trim_movie()
