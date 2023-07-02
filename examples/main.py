from youtube_uploader_selenium import YouTubeUploader

video_path = r'..\video_samples\VID_20220610_235207628.mp4'
metadata_path = r'..\video_samples\metadata.json'

video_path = r'C:\Users\philip\Documents\ai\youtube-uploader\video_samples\VID_20220610_235207628.mp4'
metadata_path = r'C:\Users\philip\Documents\ai\youtube-uploader\video_samples\metadata.json'

print(video_path)
print(metadata_path)

uploader = YouTubeUploader(video_path, metadata_path)
was_video_uploaded, video_id = uploader.upload()
assert was_video_uploaded