from VideoUploader import *
import time

videoInfo = VideoMetadata()

videoInfo.video_path = r"C:\Users\philip\Documents\ai\youtube-uploader\video-samples\good_job.mp4"
videoInfo.video_title = "My Honest Reaction"
videoInfo.video_description = "Well done."
videoInfo.video_tags = "Memes, Soylent, Internet, Redditor"
videoInfo.video_thumbnail_path = r"C:\Users\philip\Documents\ai\youtube-uploader\video-samples\gottacatchemall.jpg"

automation = YoutubeUploader(headless=True)
automation.switch_channels(channel_name="@PhilsIdeas-gh9yv")
automation.upload_video(videoInfo)
time.sleep(5)
automation.switch_channels(channel_name="@phils_stuff")
automation.upload_video(videoInfo)
automation.exit()