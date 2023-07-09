from VideoUploader import *
import time

videoInfo = VideoMetadata()

videoInfo.video_path = r"C:\Users\justi\OneDrive\Documents\GitHub\youtube-uploader\video-samples\good_job.mp4"
videoInfo.video_title = "My Honest Reaction"
videoInfo.video_description = "Well done."
videoInfo.video_tags = "Memes, Soylent, Internet, Redditor"
videoInfo.video_thumbnail_path = r"C:\Users\justi\OneDrive\Documents\GitHub\youtube-uploader\video-samples\gotta catch em all.jpg"

automation = YoutubeUploader()
#automation.setup_driver()
automation.upload_video(videoInfo)

while True:
    time.sleep(1)