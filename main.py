from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from constants import constants
from time import sleep
from logger import logger
from pathlib import Path
import os
import urllib.request
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def clear_field(field):
    field.click()
    sleep(constants.USER_WAITING_TIME)
    field.send_keys(Keys.CONTROL + 'a')
    sleep(constants.USER_WAITING_TIME)
    field.send_keys(Keys.BACKSPACE)

def write_in_field(field, string, select_all=False, getfirst=False):
    if select_all:
        clear_field(field)
    else:
        if getfirst:
            field[0].click()
        else:
            field.click()
        sleep(constants.USER_WAITING_TIME)

    field.send_keys(string)

def get_video_id(driver):
		video_id = None
		try:
			video_url_container = driver.find_element(
				By.XPATH, constants.VIDEO_URL_CONTAINER)
			video_url_element = driver.find(By.XPATH, constants.VIDEO_URL_ELEMENT, element=video_url_container)
			video_id = video_url_element.get_attribute(
				constants.HREF).split('/')[-1]
		except:
			logger.warning(constants.VIDEO_NOT_FOUND_ERROR)
			pass
		return video_id

video_path = r"C:\Users\justi\Videos\test.mp4"

VIDEO_TITLE = "Me Playing Beat Saber"
VIDEO_DESCRIPTION = "A somewhat easier song but still fast paced."
VIDEO_TAGS = "Video, Beat Saber, Oculus"

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#options.add_argument('--headless=new')
options.add_argument(r"--user-data-dir=C:\Users\justi\AppData\Local\Google\Chrome\User Data");
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get(constants.YOUTUBE_URL)
driver.maximize_window()
sleep(constants.USER_WAITING_TIME)
driver.get(constants.YOUTUBE_UPLOAD_URL)
sleep(constants.USER_WAITING_TIME)
absolute_video_path = str(Path.cwd() / video_path)
driver.find_element(By.XPATH, constants.INPUT_FILE_VIDEO).send_keys(absolute_video_path)

logger.debug('Attached video {}'.format(video_path))


# Find status container
uploading_status_container = None
while uploading_status_container is None:
    sleep(constants.USER_WAITING_TIME)
    uploading_status_container = driver.find_element(By.XPATH, constants.UPLOADING_STATUS_CONTAINER)

# TODO: Set Video Thumbnail Code
#
# if thumbnail_path is not None:
#     absolute_thumbnail_path = str(Path.cwd() / thumbnail_path)
#     driver.find(By.XPATH, constants.INPUT_FILE_THUMBNAIL).send_keys(
#         absolute_thumbnail_path)
#     change_display = "document.getElementById('file-loader').style = 'display: block! important'"
#     driver.driver.execute_script(change_display)
#     logger.debug(
#         'Attached thumbnail {}'.format(thumbnail_path))

sleep(constants.USER_WAITING_TIME * 5)
title_field, description_field = driver.find_elements(By.ID, constants.TEXTBOX_ID)

write_in_field(title_field, VIDEO_TITLE, select_all=True)
logger.debug('The video title was set to \"{}\"'.format(VIDEO_TITLE))

video_description = VIDEO_DESCRIPTION
video_description = video_description.replace("\n", Keys.ENTER)
if video_description:
    write_in_field(description_field, video_description, select_all=True)
    logger.debug('Description filled.')

# kids_section = driver.find(By.NAME, constants.NOT_MADE_FOR_KIDS_LABEL)
kids_section = driver.find_elements(By.NAME, constants.NOT_MADE_FOR_KIDS_LABEL)
kids_section[0].location_once_scrolled_into_view
sleep(constants.USER_WAITING_TIME)

driver.find_elements(By.ID, constants.RADIO_LABEL)[1].click()
logger.debug('Selected \"{}\"'.format(constants.NOT_MADE_FOR_KIDS_LABEL))

# TODO: Add functionality to add video to a playlist 
#
# playlist = metadata_dict[constants.VIDEO_PLAYLIST]
# if playlist:
#     driver.find(By.CLASS_NAME, constants.PL_DROPDOWN_CLASS).click()
#     sleep(constants.USER_WAITING_TIME)
#     search_field = driver.find(By.ID, constants.PL_SEARCH_INPUT_ID)
#     __write_in_field(search_field, playlist)
#     sleep(constants.USER_WAITING_TIME * 2)
#     playlist_items_container = driver.find(By.ID, constants.PL_ITEMS_CONTAINER_ID)
#     # Try to find playlist
#     logger.debug('Playlist xpath: "{}".'.format(constants.PL_ITEM_CONTAINER.format(playlist)))
#     playlist_item = driver.find(By.XPATH, constants.PL_ITEM_CONTAINER.format(playlist), playlist_items_container)
#     if playlist_item:
#         logger.debug('Playlist found.')
#         playlist_item.click()
#         sleep(constants.USER_WAITING_TIME)
#     else:
#         logger.debug('Playlist not found. Creating')
#         __clear_field(search_field)
#         sleep(constants.USER_WAITING_TIME)

#         new_playlist_button = driver.find(By.CLASS_NAME, constants.PL_NEW_BUTTON_CLASS)
#         new_playlist_button.click()

#         create_playlist_container = driver.find(By.ID, constants.PL_CREATE_PLAYLIST_CONTAINER_ID)
#         playlist_title_textbox = driver.find(By.XPATH, "//textarea", create_playlist_container)
#         __write_in_field(playlist_title_textbox, playlist)

#         sleep(constants.USER_WAITING_TIME)
#         create_playlist_button = driver.find(By.CLASS_NAME, constants.PL_CREATE_BUTTON_CLASS)
#         create_playlist_button.click()
#         sleep(constants.USER_WAITING_TIME)

#     done_button = driver.find(By.CLASS_NAME, constants.PL_DONE_BUTTON_CLASS)
#     done_button.click()

# Advanced options
driver.find_elements(By.ID, constants.ADVANCED_BUTTON_ID)[0].click()
logger.debug('Clicked MORE OPTIONS')
sleep(constants.USER_WAITING_TIME)

# TODO: Implement functionality to add tags to video
#
# tags = VIDEO_TAGS
# if tags:
#     # tags_container = driver.find_elements_by_id(constants.TAGS_CONTAINER_ID)
#     tags_field = driver.find_elements_by_id(constants.TAGS_INPUT)
#     write_in_field(tags_field, tags, getfirst=True)
#     logger.debug('The tags were set to \"{}\"'.format(tags))

driver.find_elements(By.ID, constants.NEXT_BUTTON)[0].click()
logger.debug('Clicked {} one'.format(constants.NEXT_BUTTON))

driver.find_elements(By.ID, constants.NEXT_BUTTON)[0].click()
logger.debug('Clicked {} two'.format(constants.NEXT_BUTTON))

driver.find_elements(By.ID, constants.NEXT_BUTTON)[0].click()
logger.debug('Clicked {} three'.format(constants.NEXT_BUTTON))

# TODO: Add functionality to schedule video upload
#
# schedule = metadata_dict[constants.VIDEO_SCHEDULE]
# if schedule:
#     upload_time_object = datetime.strptime(schedule, "%m/%d/%Y, %H:%M")
#     driver.find(By.ID, constants.SCHEDULE_CONTAINER_ID).click()
#     driver.find(By.ID, constants.SCHEDULE_DATE_ID).click()
#     driver.find(By.XPATH, constants.SCHEDULE_DATE_TEXTBOX).clear()
#     driver.find(By.XPATH, constants.SCHEDULE_DATE_TEXTBOX).send_keys(
#         datetime.strftime(upload_time_object, "%b %e, %Y"))
#     driver.find(By.XPATH, constants.SCHEDULE_DATE_TEXTBOX).send_keys(Keys.ENTER)
#     driver.find(By.XPATH, constants.SCHEDULE_TIME).click()
#     driver.find(By.XPATH, constants.SCHEDULE_TIME).clear()
#     driver.find(By.XPATH, constants.SCHEDULE_TIME).send_keys(
#         datetime.strftime(upload_time_object, "%H:%M"))
#     driver.find(By.XPATH, constants.SCHEDULE_TIME).send_keys(Keys.ENTER)
#     logger.debug(f"Scheduled the video for {schedule}")
# else:
public_main_button = driver.find_elements(By.NAME, constants.PUBLIC_BUTTON)
driver.find_elements(By.ID, constants.RADIO_LABEL)[3].click()
logger.debug('Made the video {}'.format(constants.PUBLIC_BUTTON))

video_id = get_video_id(driver)

# Check status container and upload progress
sleep(constants.USER_WAITING_TIME)

# TODO: Implement wait until upload complete, rather than waiting a hardcoded period of time
#
# uploading_status_container = driver.find_elements_by_xpath(constants.UPLOADING_STATUS_CONTAINER)
# uploading_progress = uploading_status_container.get_attribute('value')
# logger.debug('Upload video progress: {}%'.format(uploading_progress))
# sleep(constants.USER_WAITING_TIME * 5)

# logger.debug('Upload container gone.')

done_button = driver.find_elements(By.ID, constants.DONE_BUTTON)

# TODO: Implement check if submit box is greyed and unselectable 
#
# Catch such error as
# "File is a duplicate of a video you have already uploaded"
# if done_button.get_attribute('aria-disabled') == 'true':
#     error_message = driver.find_elements_by_xpath(constants.ERROR_CONTAINER).text
#     logger.error(error_message)

done_button[0].click()
sleep(constants.USER_WAITING_TIME)
driver.quit()