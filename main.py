from VideoUploader import *
import time

videoInfo = VideoMetadata()

videoInfo.video_path = r"C:\Users\Philip\Documents\programming\youtube-uploader\video-samples\good_job.mp4"
videoInfo.video_title = "My Honest Reaction"
videoInfo.video_description = "Well done."
videoInfo.video_tags = "Memes, Soylent, Internet, Redditor"

automation = YoutubeUploader()
automation.upload_video(videoInfo)
while True:
    time.sleep(1)