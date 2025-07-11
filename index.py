import os
import requests
from moviepy.editor import VideoFileClip

def download_movie(url, filename="500.mkv"):
    print("⬇️ Downloading movie...")
    response = requests.get(url, stream=True)
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print("✅ Download complete.")

def trim_movie(movie_path="500.mkv", output_folder="clips", clip_length=60):
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
