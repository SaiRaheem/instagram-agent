import os
from instagrapi import Client

def upload_clip():
    IG_USERNAME = os.getenv("IG_USERNAME")
    IG_PASSWORD = os.getenv("IG_PASSWORD")

    # 🔍 Dump environment variables for debugging
    print("\n🔍 ENVIRONMENT DUMP")
    for key in sorted(os.environ):
        if "IG" in key:
            print(f"{key} = {os.environ[key]}")
    print("🔍 END ENV DUMP\n")

    print("🔍 DEBUG IG_USERNAME =", IG_USERNAME)
    print("🔍 DEBUG IG_PASSWORD is set:", bool(IG_PASSWORD))

    if not IG_USERNAME or not IG_PASSWORD:
        raise Exception("Both username and password must be provided.")

    clips_dir = "clips"
    posted_file = "posted.txt"

    # Load history of posted clips
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

    # Initialize client and load session if available
    cl = Client()
    try:
        if os.path.exists("session.json"):
            cl.load_settings("session.json")
            print("🔐 Loaded saved session.json")
        cl.login(IG_USERNAME, IG_PASSWORD)
        print("✅ Logged in successfully")
    except Exception as e:
        print(f"⚠️ Session failed: {e}")
        print("🔁 Trying fresh login...")
        cl.login(IG_USERNAME, IG_PASSWORD)
        cl.dump_settings("session.json")
        print("✅ New session saved to session.json")

    # Upload the clip
    print(f"📤 Uploading {clip_path}")
    cl.clip_upload(clip_path, f"🔥 Check out this clip: {next_clip}")
    print(f"✅ Uploaded: {next_clip}")

    # Mark this clip as posted
    with open(posted_file, "a") as f:
        f.write(f"{next_clip}\n")
