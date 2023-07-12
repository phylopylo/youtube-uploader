from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.chrome import ChromeDriver
from selenium.webdriver.chrome.service import Service
from constants import constants
from time import sleep
from logger import logger
from pathlib import Path
import os
import urllib.request

class VideoMetadata:
    """
    A data class to store upload info about a YouTube video.

    Values
    ------
    video_path
        The filepath to the video file to be uploaded
    video_title
        The title of the video
    video_description
        The description of the video
    video_tags
        The tags for the video
    """
    def __init__(self, video_path: str = "", video_title: str = "My Video", video_description: str = "A video I made.", video_tags: str = "YouTube", video_thumbnail_path: str = ""):
        self.video_path = video_path
        self.video_title = video_title
        self.video_description = video_description
        self.video_tags = video_tags
        self.video_thumbnail_path = video_thumbnail_path

class YoutubeUploader:
    """
    An uploader for YouTube videos.

    Example Usage
    ------
    automation = YoutubeUploader()
    automation.upload_video(<VideoMetadata>)
    """

    def wait_until_elem_present(self, mode: str, selection) -> bool:
        try:
            element_present = EC.presence_of_element_located(
                (mode, selection))
            WebDriverWait(self.driver, 12).until(element_present)
            return True
        except:
            return False

    def write_in_field(self, field, string, select_all=False, getfirst=False):
        if select_all:
            field.clear()
        else:
            if getfirst:
                field[0].click()
            else:
                field.click()
            sleep(constants.USER_WAITING_TIME)
        field.send_keys(string)
    
    def __init__(self, headless: bool = False):
        self.driver = self.setup_driver(headless)

    def setup_driver(self, headless: bool = False) -> ChromeDriver:

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        if headless:
            options.add_argument('--headless=new')

        user_data_dir = str(Path.home()) + r'\AppData\Local\Google\Chrome\User Data' 
        options.add_argument('--user-data-dir=' + user_data_dir)
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        return driver
    
    def upload_video(self, metadata: VideoMetadata):
        """
        Upload a video to youtube.

        Input Parameters
        -----
        metadata
            A VideoMetadata object containing information about the video to be updated. The only necessary option is filepath, but it is reccomended to set every option.
        """

        self.driver.get(constants.YOUTUBE_URL)
        self.driver.maximize_window()
        sleep(constants.USER_WAITING_TIME)
        self.driver.get(constants.YOUTUBE_UPLOAD_URL)
        sleep(constants.USER_WAITING_TIME)
        absolute_video_path = str(Path.cwd() / metadata.video_path)
        self.driver.find_element(By.XPATH, constants.INPUT_FILE_VIDEO).send_keys(absolute_video_path)
        logger.debug('Attached video {}'.format(metadata.video_path))

        # Find status container
        uploading_status_container = None
        while uploading_status_container is None:
            self.wait_until_elem_present(By.XPATH, constants.UPLOADING_STATUS_CONTAINER)
            sleep(0.01)
            uploading_status_container = self.driver.find_element(By.XPATH, constants.UPLOADING_STATUS_CONTAINER)

        # TODO: Set Video Thumbnail Code
        #
        if metadata.video_thumbnail_path is not None:
            absolute_thumbnail_path = str(Path.cwd() / metadata.video_thumbnail_path)
            #sleep(constants.USER_WAITING_TIME * 2)
            self.wait_until_elem_present(By.XPATH, constants.INPUT_FILE_THUMBNAIL)
            self.driver.find_element(By.XPATH, constants.INPUT_FILE_THUMBNAIL).send_keys(
                absolute_thumbnail_path)
            change_display = "document.getElementById('file-loader').style = 'display: block! important'"
            self.driver.execute_script(change_display)
            logger.debug(
                'Attached thumbnail {}'.format(metadata.video_thumbnail_path))

        self.wait_until_elem_present(By.ID, constants.TEXTBOX_ID)
        title_field, description_field = self.driver.find_elements(By.ID, constants.TEXTBOX_ID)
        self.write_in_field(title_field, metadata.video_title, select_all=True)
        logger.debug('The video title was set to \"{}\"'.format(metadata.video_title))

        video_description = metadata.video_description
        video_description = video_description.replace("\n", Keys.ENTER)
        if video_description:
            self.write_in_field(description_field, video_description, select_all=True)
            logger.debug('Description filled.')

        kids_section = self.driver.find_element(By.NAME, constants.NOT_MADE_FOR_KIDS_LABEL)
        kids_section.location_once_scrolled_into_view
        sleep(constants.USER_WAITING_TIME)

        self.driver.find_elements(By.ID, constants.RADIO_LABEL)[1].click()
        logger.debug('Selected \"{}\"'.format(constants.NOT_MADE_FOR_KIDS_LABEL))

        # Advanced options
        self.driver.find_elements(By.ID, constants.ADVANCED_BUTTON_ID)[0].click()
        logger.debug('Clicked MORE OPTIONS')
        sleep(constants.USER_WAITING_TIME)
        
        tags = metadata.video_tags
        if tags:
            tags_container = self.driver.find_elements(By.ID, constants.TAGS_CONTAINER_ID)
            tags_field = self.driver.find_elements(By.ID, constants.TAGS_INPUT)
            self.write_in_field(tags_field[1], tags)
            logger.debug('The tags were set to \"{}\"'.format(tags))

        self.driver.find_elements(By.ID, constants.NEXT_BUTTON)[0].click()
        logger.debug('Clicked {} one'.format(constants.NEXT_BUTTON))

        self.driver.find_elements(By.ID, constants.NEXT_BUTTON)[0].click()
        logger.debug('Clicked {} two'.format(constants.NEXT_BUTTON))

        self.driver.find_elements(By.ID, constants.NEXT_BUTTON)[0].click()
        logger.debug('Clicked {} three'.format(constants.NEXT_BUTTON))

        public_main_button = self.driver.find_elements(By.NAME, constants.PUBLIC_BUTTON)
        self.driver.find_elements(By.ID, constants.RADIO_LABEL)[3].click()
        logger.debug('Made the video {}'.format(constants.PUBLIC_BUTTON))

        # Check status container and upload progress
        sleep(constants.USER_WAITING_TIME)

        # TODO: Implement wait until upload complete, rather than waiting a hardcoded period of time
        #
        # uploading_status_container = driver.find_elements_by_xpath(constants.UPLOADING_STATUS_CONTAINER)
        # uploading_progress = uploading_status_container.get_attribute('value')
        # logger.debug('Upload video progress: {}%'.format(uploading_progress))
        # sleep(constants.USER_WAITING_TIME * 5)

        # logger.debug('Upload container gone.')

        done_button = self.driver.find_elements(By.ID, constants.DONE_BUTTON)

        # TODO: Implement check if submit box is greyed and unselectable 
        #
        # Catch such error as
        # "File is a duplicate of a video you have already uploaded"
        # if done_button.get_attribute('aria-disabled') == 'true':
        #     error_message = driver.find_elements_by_xpath(constants.ERROR_CONTAINER).text
        #     logger.error(error_message)

        done_button[0].click()
        sleep(100)
        self.driver.quit()
    
# def switch_channels(driver, channel_name: str):
#     AVATAR_MENU = "avatar-btn"
#     SWITCH_CHANNEL = ""
#     driver.find(By.XPATH, )

if __name__ == "__main__":
    logger.error("VideoUploader does not have a main function. Are you sure you are running the correct file?")