"""
YouTube Video Uploader Tool
Authors: Philip Roberts and Justin Bell

======================================================================

                    YouTube Video Uploader

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
    USA

======================================================================
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.chrome import ChromeDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import urllib.request
from constants import constants
from logger import logger
from pathlib import Path
import time
import os

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
        """
        A function that waits until an element is present and should be used as a buffer between actions so that code is not executed before
        an element is present

        Input Parameters
        -----
            mode
                the attribute that can be accessed by selenium which can be XPATH, ID, Class, etc
            selection
                the specific element on the webpage that can be accessed
        Return Value
        -----
            returns bool
        """
        try:
            element_present = EC.presence_of_element_located(
                (mode, selection))
            WebDriverWait(self.driver, 12).until(element_present)
            return True
        except:
            return False

    def write_in_field(self, field, string, select_all=False, getfirst=False):
        """
        A function that writes in a field or search bar spefically and enters in text

        Input Parameters
        ------------
            field 
                the field the string will be inputted to (could be a search bar)
            string
                a string of text to enter into the field
            select_all
                selects all fields if there is a list of fields
            getfirst
                only selects the first field if there is a list of fields
        """
        if select_all:
            field.clear()
        else:
            if getfirst:
                field[0].click()
            else:
                field.click()
            time.sleep(constants.USER_WAITING_TIME)
        field.send_keys(string)
    
    def __init__(self, headless: bool = False):
        """
        a python __init__ function

        Input Parameters
        ------
            headless
                a bool that is true when the application is headless
        """
        self.driver = self.setup_driver(headless)

    def setup_driver(self, headless: bool = False) -> ChromeDriver:
        """
        Sets up the ChromeDriver which can be ran either headless or using your default chrome account

        Input Parameters
        ----
            headless
                a boolean stating whether the ChromeDriver should be headless or not (WIP)
        Return Value
        ----
            returns a ChromeDriver object
        """
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        if headless:
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')


        #Adds your deafault Chrome Account as the user data directory for the application
        user_data_dir = str(Path.home()) + r'\AppData\Local\Google\Chrome\User Data' 
        options.add_argument('--user-data-dir=' + user_data_dir)
        
        #Creates the driver
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
        time.sleep(constants.USER_WAITING_TIME)
        self.driver.get(constants.YOUTUBE_UPLOAD_URL)
        time.sleep(constants.USER_WAITING_TIME)
        absolute_video_path = str(Path.cwd() / metadata.video_path)
        self.driver.find_element(By.XPATH, constants.INPUT_FILE_VIDEO).send_keys(absolute_video_path)
        logger.debug('Attached video {}'.format(metadata.video_path))

        # Find status container
        uploading_status_container = None
        while uploading_status_container is None:
            self.wait_until_elem_present(By.XPATH, constants.UPLOADING_STATUS_CONTAINER)
            time.sleep(0.01)
            uploading_status_container = self.driver.find_element(By.XPATH, constants.UPLOADING_STATUS_CONTAINER)

        # TODO: Set Video Thumbnail Code
        #
        if metadata.video_thumbnail_path is not None:
            absolute_thumbnail_path = str(Path.cwd() / metadata.video_thumbnail_path)
            #time.sleep(constants.USER_WAITING_TIME * 2)
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
        time.sleep(constants.USER_WAITING_TIME)

        self.driver.find_elements(By.ID, constants.RADIO_LABEL)[1].click()
        logger.debug('Selected \"{}\"'.format(constants.NOT_MADE_FOR_KIDS_LABEL))

        # Advanced options
        self.driver.find_elements(By.ID, constants.ADVANCED_BUTTON_ID)[0].click()
        logger.debug('Clicked MORE OPTIONS')
        time.sleep(constants.USER_WAITING_TIME)
        
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
        upload_complete = False
        while not upload_complete:
            upload_status = self.driver.find_elements(By.CLASS_NAME, "progress-label.style-scope.ytcp-video-upload-progress")
            print(upload_status[0].text)
            upload_complete = "Checks complete. No issues found." in upload_status[0].text
            time.sleep(0.1)

        time.sleep(constants.USER_WAITING_TIME)
        done_button = self.driver.find_elements(By.ID, constants.DONE_BUTTON)
        done_button[0].click()
        time.sleep(constants.USER_WAITING_TIME)
        # self.driver.close()
    
    def switch_channels(self, channel_name: str):
        """
        Switches the current channel you are on with channel_name
        
        Input Parameters
        ------
            channel_name: a string that is the channel name of the channel that will be switched to.
        """

        # Open the channel switching page on YouTube, and wait until it is completely loaded.
        self.driver.get(constants.CHANNEL_SWITCH_URL)
        self.wait_until_elem_present(By.ID, 'contents')

        # Once the contents div exists, find the container for the channel switcher
        channel_switcher = self.driver.find_elements(By.ID, 'contents')[2]

        # If the loop didn't find the channel switcher, throw an exception.
        if channel_switcher is None:
            raise Exception("Channel Switcher not found.")
        
        # Loop through each channel div, and when the channel div contains the YouTube tag of the channel to be switched to, click on it.
        for channel in channel_switcher.find_elements(By.XPATH, ".//*"):
            
            if(channel_name in channel.text):
                channel.click()
                print("Switched to channel " + channel_name)
                break

        time.sleep(1)

        # Confirm that the channel switched successfully

        # Open the YouTube homepage, click on the avatar profile picture, and confirm that the channel name is within the dialog box.
        self.driver.get(constants.YOUTUBE_URL)
        self.wait_until_elem_present(By.ID, "avatar-btn")
        self.driver.find_elements(By.ID, "avatar-btn")[0].click()

        self.wait_until_elem_present(By.ID, "channel-handle")
        dialog_boxes = self.driver.find_elements(By.ID, "channel-handle")
        
        for dialog in dialog_boxes:
            print(dialog.text)
            if channel_name in dialog.text:
                print("Channel Switch Confirmed")
                return True

        raise Exception("Channel Switch Failure")
    
    def exit(self):
        self.driver.quit()

if __name__ == "__main__":
    logger.error("VideoUploader does not have a main function. Are you sure you are running the correct file?")