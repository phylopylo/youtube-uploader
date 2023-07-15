# youtube-uploader
  Automation for YouTube video uploading. Utilizes a headless Selenium web browser to upload YouTube Videos to one or more YouTube Channels.
## Prerequisites
   to get the modules needed run
    ```
      pip install -r requirments.txt
    ```
    or install these modules
      logger 1.4,
      selenium 4.10,
      webdrvier_manager 3.8.6
### Selenium Webdriver
  if not done already install a selenium chromedriver
      the specific version used for this project is Chome Driver 93.0.4577.63
      and can be found here
      https://chromedriver.chromium.org/downloads
      
      
  ## Basic Functionality
  ```
  To use the application to upload a video first create a VideoMetadata values:
    videoInfo = VideoMetadata()
  ```
  Then add values to the VideoMetadata() values
  ```
    videoInfo.video_path = your/video/path
    videoInfo.video_title = "video title"
    videoInfo.video_title = "video description"
    videoInfo.video_thumbnail_path = your/thumbnail/path
  ```
  Then create the VideoUploader() object to upload your video
  ```
    automation = VideoUploader()
  ```
  To upload a video do
  ```
    automation.upload_video(videoInfo)
  ```
  to switch channels
  ```
    automation.switch_channels(channel_name="@channelName")
  ```
  exiting the program
  ```
    automation.exit()
  ```

