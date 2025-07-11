import os
os.makedirs("clips", exist_ok=True)  # ✅ Ensure folder exists on Railway

from instagrapi import Client
from dotenv import load_dotenv
import random

load_dotenv()
from instagrapi import Client
import os
from dotenv import load_dotenv

load_dotenv()

def upload_clip():
    username = os.getenv("IG_USERNAME")
    password = os.getenv("IG_PASSWORD")

    posted_file = "posted.txt"
    clips_dir = "clips"

    # Read posted clips
    posted = set()
    if os.path.exists(posted_file):
        with open(posted_file, "r") as f:
            posted = set(line.strip() for line in f.readlines())

    # Find next unposted clip
    clips = sorted([c for c in os.listdir(clips_dir) if c.endswith(".mp4")])
    for clip in clips:
        if clip not in posted:
            clip_path = os.path.join(clips_dir, clip)
            caption = f"Clip: {clip}"

            # Upload using instagrapi
            cl = Client()
            cl.login(username, password)
            cl.clip_upload(clip_path, caption)

            # Save to posted list
            with open(posted_file, "a") as f:
                f.write(f"{clip}\n")
            print(f"✅ Uploaded: {clip}")
            break
    else:
        print("🎉 All clips uploaded.")
