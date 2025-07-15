from moviepy.editor import VideoFileClip

clip = VideoFileClip("test.mkv").subclip(0, 5)  # 5-sec test
output = "test_out.mp4"

clip.write_videofile(
    output,
    codec="libx264",
    audio=True,
    ffmpeg_params=[
        "-vf", "transpose=1",  # just rotation
        "-crf", "23",
        "-preset", "ultrafast"
    ]
)
