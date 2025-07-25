import os
import time
from index import download_movie, trim_movie
from uploader import upload_clip

while True:
    try:
        if not os.path.exists("video.mp4"):
            download_movie()
        
        if not os.path.exists("clips") or not os.listdir("clips"):
            trim_movie()
        
        upload_clip()
        
    except Exception as e:
        print(f"Error: {e}")
    
    time.sleep(60 * 60)  # Check hourly