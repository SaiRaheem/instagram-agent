from moviepy.editor import VideoFileClip
import os

def trim_movie(movie_path, output_folder="clips", clip_length=60, max_clips=5):
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
        subclip.write_videofile(output_path, codec='libx264', audio=False, logger=None)
        count += 1

if __name__ == "__main__":
    trim_movie("500.mkv")
import requests

def download_movie(url="https://drive.google.com/uc?export=download&id=1jP_09FYxyb1QZhzwWzglHRWS8ZaRZnso", dest="500.mkv"):
    response = requests.get(url, stream=True)
    with open(dest, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
