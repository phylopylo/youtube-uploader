from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from constants import constants
from time import sleep

options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=C:\Users\philip\AppData\Local\Google\Chrome\User Data");
options.add_argument(r'--profile-directory=C:\Users\philip\AppData\Local\Google\Chrome\User Data\Default')


driver = webdriver.Chrome(options=options)
driver.get(constants.YOUTUBE_URL)
sleep(constants.USER_WAITING_TIME)
input()
print(driver.get_cookies())
