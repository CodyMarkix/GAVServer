import seleniumrequests as selenreq
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import base64

import shutil, time, random

from config import Config

class Session:
    def __init__(self, config: Config, mail: str, password: str):
        self.config = config
        self.__mail = mail
        self.__password = password

        geckodriver_path = shutil.which('geckodriver')
        if geckodriver_path == None:
            geckodriver_path = ""

        # Initialize Firefox driver
        service = Service(geckodriver_path)

        options = Options()
        options.binary_location = config.getFirefoxBinary()

        self.browser = selenreq.Firefox(service=service, options=options)
        self.serverURL = self.config.getServerURL()

        self.logged_in_page = self.login()

    def __str__(self):
        return f"Mail: {self.__mail}; Password: {base64.b64encode(self.__password.encode()).decode()}"

    def calculateGoogleDelay(self, base_delay: int, offset: float) -> float:
        base_delay_float = float(base_delay)
        return random.uniform(base_delay_float - offset, base_delay_float + offset)

    def login(self):
        creds = (self.__mail, self.__password)
        delays = self.config.getDelays()

        # Navigating the server website
        self.browser.get(self.serverURL)
        self.browser.find_element(By.ID, 'j_idt21:login').send_keys(Keys.ENTER)
        time.sleep(delays[0])

        self.browser.find_element(By.TAG_NAME, 'button').send_keys(Keys.ENTER)
        time.sleep(delays[0])

        #------------------------
        # GOOGLE AUTHENTICATION
        #------------------------
        email_field = self.browser.find_element(By.ID, 'identifierId')
        email_field.send_keys(creds[0])
        time.sleep(self.calculateGoogleDelay(delays[1], delays[2])) # We have to be a lot more careful as to not trip up any bot detection Google might have
        email_field.send_keys(Keys.ENTER)
        time.sleep(self.calculateGoogleDelay(delays[1], delays[2]))

        pass_field = self.browser.find_element(By.NAME, 'Passwd')
        pass_field.send_keys(creds[1])
        time.sleep(self.calculateGoogleDelay(delays[1], delays[2]) + 1)
        pass_field.send_keys(Keys.ENTER)
        time.sleep(self.calculateGoogleDelay(delays[1], delays[2]) + 1.75)

        # Returning the signed in homepage
        logged_in_homepage = self.browser.page_source
        time.sleep(0.5)

        return logged_in_homepage
    
    def getUserFullName(self) -> list[str]:
        self.browser.get(self.serverURL + "/index.xhtml")
        time.sleep(0.5)

        fullNameDiv = self.browser.find_element(By.CLASS_NAME, 'title_text_right')

        with open('debug.html', 'w', encoding='utf-8') as f:
            f.write(self.browser.page_source)
        
        # sanitize the results of any encoding fuckers
        result = fullNameDiv.find_element(By.TAG_NAME, 'span').text.split(" ")[:-1]
        result_sanitized = []
        for x in result:
            result_sanitized.append(x.encode(encoding='utf-8').decode(encoding='utf-8'))

        return result_sanitized
    
    def getSeminars(self) -> list:
        # TODO: Find someone who has seminars and ask them for a copy of https://vyuka.gyarab.cz/seminare/
        self.browser.get(self.serverURL + "/seminare")
        time.sleep(0.5)

        if "Pro Vaši skupinu nejsou momentálně k dispozici žádné semináře." in self.browser.page_source.encode().decode():
            return []
        else:
            return ["garbage data"]
        