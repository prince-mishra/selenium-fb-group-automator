"""Main module."""

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
os.environ["LANG"] = "en_US.UTF-8"

FB_LOGIN_URL = "https://www.facebook.com"
FB_GROUP_PREFIX = "https://www.facebook.com/groups/"

class FBSeleniumDriver():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = self.init_driver()
        
    
    def init_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2 # 1:allow, 2:block 
        })

        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(15) # seconds
        return driver


class FBGroupPoster():
    def __init__(self, username, password):
        # Get the Chrome driver and login
        self.username = username
        self.password = password
        self.fbdriver = FBSeleniumDriver(username, password)

    def login(self):
        self.fbdriver.driver.get(FB_LOGIN_URL)
        self.fbdriver.driver.implicitly_wait(15)    
        # Enter user email
        elem = self.fbdriver.driver.find_element_by_id("email")
        elem.send_keys(self.username)
        # Enter user password
        elem = self.fbdriver.driver.find_element_by_id("pass")
        elem.send_keys(self.password)
        # Login
        elem.send_keys(Keys.RETURN)
        self.fbdriver.driver.implicitly_wait(15)
        sleep(10)

    def visit_group(self, group):
        self.fbdriver.driver.get(FB_GROUP_PREFIX + group)
        self.fbdriver.driver.implicitly_wait(15)
    
    def submit_text(self, text):
        post_box = self.fbdriver.driver.find_element_by_xpath("//*[@name='xhpc_message_text']")
        # Enter the text we want to post to Facebook
        post_box.send_keys(text)
        buttons = self.fbdriver.driver.find_elements_by_tag_name("button")
        sleep(5)
        for button in buttons:
            if button.text == "Post":
                sleep(10)
                button.click()
                sleep(10)
    
    def submit_image_and_text(self, text, img_path):
        post_box = self.fbdriver.driver.find_element_by_xpath("//*[@name='xhpc_message_text']")
        # Enter the text we want to post to Facebook
        post_box.send_keys(text)

        addMediaButton = self.fbdriver.driver.find_elements_by_xpath("//*[contains(text(), 'Photo/Video')]")[0]
        addMediaButton.click()
        sleep(10)
        self.fbdriver.driver.find_element_by_xpath("//div[text()='Upload Photos/Videos']/following-sibling::div/input").send_keys(img_path)
        # Wait for the image to upload
        sleep(10)
        buttons = self.fbdriver.driver.find_elements_by_tag_name("button")
        for button in buttons:
            if button.text == "Post":
                sleep(10)
                button.click()
                sleep(10)
