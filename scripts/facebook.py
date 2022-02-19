from concurrent.futures import thread
import imp
from optparse import Values
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import xlsxwriter
import time
import os
import sys
import threading
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import json
from selenium.common.exceptions import (
    ElementClickInterceptedException, StaleElementReferenceException, NoSuchElementException, InvalidArgumentException
)
import pickle as pickle
import multiprocessing
from playsound import playsound
from resources.mails.cache import cachedata

# Global variable
linksCount = 0

BASE_PATH = os.path.dirname(sys.executable)
if 'DJANGO_DEVELOPMENT' in os.environ:
    BASE_PATH = './'


def get_path(filepath):
    return os.path.join(BASE_PATH, filepath)


class MyListener(AbstractEventListener):

    def __init__(self, config):
        self.config = config


class FB_WhatsappBot(object):
    def __init__(self):
        playsound('resources/sounds/start.wav')
        data = self.openlogins()
        print("\n Login Data Retrieved successfully...")
        sys.stdout.write("\n in the init function...")
        self.urlList = []     
        self.deleting = "NotDeleting"
        self.thread_count = int(data['threadCount'])
        self.email_1 = data['username']
        self.password_1 = data['password']
        self.n_scrolls = int(data['scrolls'])
        self.state = data['state']
        self.KeyWord = "whatsapp group"
        self.browser = 'chrome'

    def openlogins(self):
        with open('resources/PickleFiles/logins.pkl', 'rb') as f:
            data = pickle.load(f)
            return data

    def get_driver(self):
        chrome_options = webdriver.ChromeOptions()
        headstate = self.state
        if headstate == "Headless":
            print("\n he state chosen is: ", self.state, "\n", "The bot should go headless")
            chrome_options.add_argument('headless')
        else:
            print("\n the state chosen is: ", self.state, "\n", "Showing browser window")
            pass
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument("--disable-logging")
        driver = webdriver.Chrome(options=chrome_options)
        # driver.set_window_size(1020, 690)
        #   driver = webdriver.Chrome(options=chrome_options, executable_path="D:/bot/fb/chromedriver.exe")  # USER INPUT
        driver.maximize_window()
        return driver

    def flush_then_wait(self):
        sys.stdout.flush()
        sys.stderr.flush()
        time.sleep(0.5)

    def init_bot(self):
        sys.stdout.write("\n Hold On")
        for x in range(0, self.thread_count): 
            driver = self.get_driver()
            # self.thread = multiprocessing.Process(target=self.login, args=(driver,), name="thread_{}".format(x), )
            thread = threading.Thread(target=self.login, args=(driver,), name="thread_{}".format(x), )
            thread.daemon = False
            thread.start()
            time.sleep(3)

    def get_links(self):

        file = open("resources/PickleFiles/facebookUrlsList.pkl", "rb")

        file_lines = pickle.load(file)
        list_of_lines = file_lines.split("\n")
        return list_of_lines

    def login(self, driver):
        sys.stdout.write("\n Attempting Login...")
        try:
            driver.get('https://www.facebook.com/')
            email = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name = 'email']")))
            password = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name = 'pass']")))

            sys.stdout.write("\n clearing Login Form...")
            email.clear()
            password.clear()
            sys.stdout.write("\n Filling Login form...")
            email.send_keys(self.email_1)  # USER INPUT
            password.send_keys(self.password_1)  # USER INPUT

            sys.stdout.write("\n Logging in now...")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[type = 'submit']"))).click()
        finally:
            self.setup_Keyword(driver)

    def close(self, driver):
        global linksCount
        if threading.active_count() == 1:
            cachedata()
        playsound('resources/sounds/ending.wav')
        print("\n Closing browser and found ", linksCount, " whatsapp links")
        driver.close()

    def setup_Keyword(self, driver):

        x = self.KeyWord  # USER INPUT
        sys.stdout.write("\n removing white spaces...")
        x = x.replace(" ", "%20")
        try:
            if self.deleting == "Deleting":
                time.sleep(3)
            else:
                pass
        finally:
            print("\n Free to open new window")
        self.deleting = "Deleting"
        group_link_1 = self.get_links()[0]
        sys.stdout.write("\n Getting Group Link...")
        group_link = f"{group_link_1}/search/?q={x}"
        try:
            time.sleep(3)
            driver.get(f"{group_link}")  # USER INPUT
            # time.sleep(3)
            print("\n opening Link: {}", format(group_link))
        except InvalidArgumentException:
            sys.stdout.write("\n done getting links...")
            self.close(driver)

        self.delete_used_link(driver)
        self.search_Keyword(driver)

    def delete_used_link(self, driver):

        a_file = open("resources/PickleFiles/facebookUrlsList.pkl", "rb")
        lines = pickle.load(a_file)
        a_file.close()
        try:
            del lines[0]
        except IndexError:
            print("\n NO links lefts to use")
            self.close(driver)

        new_file = open("resources/PickleFiles/facebookUrlsList.pkl", "wb")
        for line in lines:
            pickle.dump(line, new_file)
        new_file.close()
        self.deleting = "NotDeleting"
        

    def search_Keyword(self, driver):
        urls = []
        count = 0
        for i in range(1, self.n_scrolls):
            count = count
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            count += 1
            print("\n Scrolling :", count)
            time.sleep(5)
            global linksCount
            linksCount = 0
            elems = driver.find_elements_by_xpath("//a[@href]")
            for elem in elems:
                try:
                    url_string = elem.get_attribute("href")
                    if "chat" in url_string and "com" in url_string and "whatsapp" in url_string:
                        print("\n Hooraaaayy....link", "\n", "\n", url_string, " is a whatsapp link")
                        self.urlList.append(url_string)
                        playsound('resources/sounds/foundLink.wav')
                        linksCount +=1
                        self.processData( url_string)
                    else:
                        pass
                        # print("\n link", "\n", "\n", url_string, " is not a whatsapp link...")
                except StaleElementReferenceException:
                    sys.stdout.write("\n did not find a link here...")
        count = 0
        self.setup_Keyword(driver)


    def processData(self, url_string):
        global linksCount
        print("Trying to save data now")
        try:
            with open("resources/whatsAppUrls.txt", "a") as f:
                f.write(f"{url_string} \n \n")
                f.close()
        finally:
            print("Done saving data")








if __name__ == '__main__':
    ed = FB_WhatsappBot()
    sys.stdout.write("\n The bot is now starting...")
    ed.init_bot()
