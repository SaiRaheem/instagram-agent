import gdown
from moviepy.editor import VideoFileClip
import os

def download_movie(file_id, output="500.mkv"):
    print("⬇️ Downloading using gdown...")
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output, quiet=False)

def trim_movie(movie_path, output_folder="clips", clip_length=60):
    os.makedirs(output_folder, exist_ok=True)
    clip = VideoFileClip(movie_path)
    duration = int(clip.duration)

    count = 0
    for start in range(0, duration, clip_length):
        end = min(start + clip_length, duration)
        subclip = clip.subclip(start, end)
        output_path = os.path.join(output_folder, f"clip_{count:04d}.mp4")
        subclip.write_videofile(output_path, codec='libx264')
        count += 1
