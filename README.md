# youtube-uploader
  Automation for YouTube video uploading. Utilizes a Selenium web browser to upload YouTube Videos to one or more YouTube Channels.
## Prerequisites
  First, ensure that the [Chrome web browser](https://www.google.com/chrome/) is installed on your system.

  To install dependencies, run:
  `pip install -r requirements.txt`
  or install these modules:
  - logger==1.4
  - selenium==4.10.0
  - webdriver_manager==3.8.6

  ## Basic Functionality
  First, import every function from VideoUploader.
  ```
  from VideoUploader import *
  ```
  Create a VideoMetadata object, which will contain the information about the video to be uploaded.
  ```
    videoInfo = VideoMetadata()
  ```
  Then, set these values in the VideoMetadata object.
  ```
    videoInfo.video_path = "C:\\path\to\your\video"
    videoInfo.video_title = "video title"
    videoInfo.video_title = "video description"
    videoInfo.video_thumbnail_path = "C:\\path\to\your\thumbnail_image"
  ```
  Then, create a VideoUploader. This object manages the video uploading.
  ```
    automation = VideoUploader()
  ```
  To upload a video, run:
  ```
    automation.upload_video(videoInfo)
  ```
  To switch between YouTube channels, run:
  ```
    automation.switch_channels(channel_name="@channelName")
  ```
  Once you have finished uploading video(s), close the WebDriver with:
  ```
    automation.exit()
  ```
  ## Complete example
  ```
  from VideoUploader import *
  import time

  videoInfo = VideoMetadata()

  videoInfo.video_path = r"C:\path\to\video"
  videoInfo.video_title = "My amazing video!"
  videoInfo.video_description = "This is the description for my video."
  videoInfo.video_tags = "YouTube, Cool Videos, Selenium"
  videoInfo.video_thumbnail_path = r"C:\\path\to\thumbnail"

  automation = YoutubeUploader()
  automation.switch_channels(channel_name="@channel-name")
  automation.upload_video(videoInfo)
  time.sleep(5)
  automation.switch_channels(channel_name="@channel-name")
  automation.upload_video(videoInfo)
  automation.exit()
  ```
  ## Authors
  This software was written by Philip Roberts and Justin Bell.

  [Check out my website!](http://philip.roberts.ws/)