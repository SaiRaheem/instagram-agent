import os
from instagrapi import Client

def upload_clip():
    IG_USERNAME = os.getenv("IG_USERNAME")
    IG_PASSWORD = os.getenv("IG_PASSWORD")

    if not IG_USERNAME or not IG_PASSWORD:
        raise Exception("Both username and password must be provided.")

    clips_dir = "clips"
    posted_file = "posted.txt"

    # Load posted history
    posted = set()
    if os.path.exists(posted_file):
        with open(posted_file, "r") as f:
            posted = set(f.read().splitlines())

    # Find next clip to upload
    all_clips = sorted([f for f in os.listdir(clips_dir) if f.endswith(".mp4")])
    next_clip = next((f for f in all_clips if f not in posted), None)

    if not next_clip:
        print("🎉 All clips have been uploaded.")
        return

    clip_path = os.path.join(clips_dir, next_clip)

    # Upload
    print(f"📤 Uploading {clip_path}")
    cl = Client()
    cl.login(IG_USERNAME, IG_PASSWORD)
    cl.clip_upload(clip_path, f"🔥 Check out this clip: {next_clip}")
    print(f"✅ Uploaded: {next_clip}")

    # Save to posted.txt
    with open(posted_file, "a") as f:
        f.write(f"{next_clip}\n")
