import os
import subprocess
import gdown
from moviepy.editor import VideoFileClip

MOVIE_URL = "https://drive.google.com/uc?id=1kuTuAhJV3DxpufNi0riijj8ub0q2FDkt"
MOVIE_PATH = "test.mkv"
CLIPS_DIR = "clips"
CLIP_DURATION = 30
MAX_CLIPS = 1

# FFmpeg filter chain
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
    print("✂️ Trimming into raw clips...")
    os.makedirs(output_folder, exist_ok=True)

    clip = VideoFileClip(movie_path)
    duration = int(clip.duration)
    count = 0

    for start in range(0, duration, clip_length):
        if count >= max_clips:
            break

        end = min(start + clip_length, duration)
        subclip = clip.subclip(start, end)
        raw_output = os.path.join(output_folder, f"clip_{count:04d}_raw.mp4")
        final_output = os.path.join(output_folder, f"clip_{count:04d}.mp4")

        print(f"🎞 Exporting raw clip: {raw_output}")
        subclip.write_videofile(
            raw_output,
            codec="libx264",
            audio=True,
            preset="ultrafast",
            logger="bar"
        )

        # Apply filters using FFmpeg
        print(f"🎨 Enhancing clip with FFmpeg filters: {final_output}")
        cmd = [
            "ffmpeg", "-y",
            "-i", raw_output,
            "-vf", FILTERS,
            "-c:v", "libx264",
            "-crf", "20",
            "-preset", "slow",
            "-c:a", "copy",
            final_output
        ]
        subprocess.run(cmd, check=True)

        # Clean up raw file
        os.remove(raw_output)
        count += 1

    print(f"✅ Done. {count} filtered clip(s) created.")
