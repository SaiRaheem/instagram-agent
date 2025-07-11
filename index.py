from moviepy.editor import VideoFileClip
import os

# === Settings ===
MOVIE_PATH = r"C:\Users\saira\OneDrive\Pictures\PHONE\IDK\500.mkv"
OUTPUT_FOLDER = "clips"
CLIP_LENGTH = 60  # seconds

def trim_video(movie_path, clip_length, out_folder):
    # Create folder if not exists
    os.makedirs(out_folder, exist_ok=True)

    print(f"Loading video from {movie_path}...")
    clip = VideoFileClip(movie_path)
    total_clips = int(clip.duration // clip_length)

    print(f"Total clips to generate: {total_clips}")

    for i in range(total_clips):
        start = i * clip_length
        end = start + clip_length
        print(f"Creating clip {i+1} from {start}s to {end}s")
        
        subclip = clip.subclip(start, end)
        subclip_path = os.path.join(out_folder, f"clip_{i+1:03}.mp4")
        subclip.write_videofile(subclip_path, codec="libx264", audio_codec="aac")

    print("✅ Done splitting video!")

# Run the trimming
trim_video(MOVIE_PATH, CLIP_LENGTH, OUTPUT_FOLDER)
