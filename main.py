from VideoUploader import *
import time

videoInfo = VideoMetadata()

videoInfo.video_path = r"C:\Users\justi\OneDrive\Documents\GitHub\youtube-uploader\video-samples\good_job.mp4"
videoInfo.video_title = "My Honest Reaction"
videoInfo.video_description = "Well done."
videoInfo.video_tags = "Memes, Soylent, Internet, Redditor"
videoInfo.video_thumbnail_path = r"C:\Users\justi\OneDrive\Documents\GitHub\youtube-uploader\video-samples\gottacatchemall.jpg"

automation = YoutubeUploader()
automation.upload_video(videoInfo)
