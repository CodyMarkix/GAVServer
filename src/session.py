from outcome import Value
import seleniumrequests as selenreq
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

import subprocess
from datetime import datetime, timedelta
import shutil, time, random, os
import base64

from config import Config

class Session:
    def __init__(self, config: Config, mail: str, password: str, id: int, cookies=None, local_storage=None, session_storage=None):
        self.config = config
        self.mail = mail
        self.__password = password
        self.id = id
        # TODO: Make sure that you can do simultaneous requests

        if "GAV_DEBUG_MODE" in os.environ.keys():
            if os.environ['GAV_DEBUG_MODE'] != "true":
                os.environ['MOZ_HEADLESS'] = "1"
        elif self.config.getHeadlessMode():
            os.environ['MOZ_HEADLESS'] = "1"
        else:
            print("Geckodriver running in head mode!")

        geckodriver_path = shutil.which('geckodriver')
        if geckodriver_path == None:
            geckodriver_path = ""

        # Initialize Firefox driver
        self.gecko_service = Service(geckodriver_path, popen_kw={"creation_flags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == 'nt' else {})

        self.browser_options = Options()
        self.browser_options.binary_location = config.getFirefoxBinary()

        self.browser = selenreq.Firefox(service=self.gecko_service, options=self.browser_options)
        
        if all([cookies != None, local_storage != None, session_storage != None]):
            self.serverURL = self.config.getServerURL()
            self.browser.get(self.serverURL + "/index.xhtml")
            
            # Resuming a session if necessary
            self.browser.delete_all_cookies()
            for cookie in cookies:
                self.browser.add_cookie(cookie)

            for key, value in local_storage.items():
                self.browser.execute_script(f"window.localStorage.setItem('{key}', '{value}');")

            for key, value in session_storage.items():
                self.browser.execute_script(f"window.sessionStorage.setItem('{key}', '{value}');")

            self.browser.refresh()
        else:
            self.serverURL = self.config.getServerURL()
            self.logged_in_page = self.login()

    def __str__(self):
        return f"Mail: {self.mail}; Password: [REDACTED]"
    
    @staticmethod
    def getCurrentSemester(academic_year: str): # https://chatgpt.com/share/674c1ea5-1cac-8003-bf74-bff0b104960b
        try:
            start_year, end_year = map(int, academic_year.split('/'))
            if end_year - start_year != 1:
                raise ValueError("Invalid academic year range.")
            base_year = 2011
            return start_year - base_year
        except Exception:
            return "" # Modified this because I am not about to handle exceptions at a server level. At least not right now

    @staticmethod
    def getSchoolYearByTime() -> str:
        current_date = datetime.now()
        return f"{current_date.year}/{int(str(current_date.year)[2:]) + 1}"

    @staticmethod
    def calculateGoogleDelay(base_delay: int, offset: float) -> float:
        base_delay_float = float(base_delay)
        return random.uniform(base_delay_float - offset, base_delay_float + offset)
    
    @staticmethod
    def convertDayMonthToDate(input: str) -> str:
        now = datetime.now()
        input_day = float(input.strip(".").split(" ")[0])
        input_month = float(input.strip(".").split(" ")[1])

        try:
            if input_month > 8:
                if now.month < 7:
                    return f"{input} {now.year - 1}"
                else:
                    return f"{input} {now.year}"
            else:
                if now.month < 7:
                    return f"{input} {now.year}"
                else:
                    raise ValueError()
        except ValueError:
            return ""

    def login(self):
        creds = (self.mail, self.__password)
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

        # Going to Google My Account, we're gonna quickly scrape the avatar
        # self.browser.get("https://myaccount.google.com")
        # time.sleep(delays[1] + 2)

        # God I love web scraping so so much
        # avatar_url = self.browser.find_element(By.CLASS_NAME, 'pGxpHc').find_element(By.TAG_NAME, 'header').find_element(By.CLASS_NAME, 'gb_kd gb_od gb_Fd').find_element(By.CLASS_NAME, 'gb_Bd gb_Zd gb_wd gb_Jd').find_element(By.CLASS_NAME, 'gb_Re').find_element(By.CLASS_NAME, 'gb_y gb_bd gb_Nf gb_Z').find_element(By.CLASS_NAME, 'gb_C gb_ib gb_Nf gb_Z').find_element(By.CLASS_NAME, 'gb_A gb_Xa gb_Z').find_element(By.CLASS_NAME, 'gb_O gbii').get_attribute('src')
        # self.avatar = base64.b64encode(self.browser.request('GET', avatar_url).content)

        self.browser.get(self.serverURL)
        time.sleep(0.25)
    
    def getUserFullName(self) -> list[str]:
        self.browser.get(self.serverURL + "/index.xhtml")
        time.sleep(self.config.getDelays()[0])

        fullNameDiv = self.browser.find_element(By.CLASS_NAME, 'title_text_right')
        
        # sanitize the results of any encoding fuckers
        # what the fuck kinda encoding is selenium using that results in correct but incorrectly capitalized characters
        result = fullNameDiv.find_element(By.TAG_NAME, 'span').text.split(" ")[:-1]
        result_sanitized = []
        for x in result:
            result_sanitized.append(x.capitalize())

        return result_sanitized
    
    def getUserGoogleAvatar(self) -> bytes:
        google_url = "https://myaccount.google.com"
        self.browser.get(google_url)
        time.sleep(self.config.getDelays()[1] + 3)

        acc_change_element = self.browser.find_element(By.CLASS_NAME, 'gb_A gb_Xa gb_Z')
        image_element = acc_change_element.find_element(By.TAG_NAME, 'img')
        
        return self.browser.request('GET', image_element.get_attribute('src')).content
    
    def getClass(self) -> str:
        self.browser.get(self.serverURL + "/index.xhtml")
        time.sleep(self.config.getDelays()[0])

        fullNameDiv = self.browser.find_element(By.CLASS_NAME, 'title_text_right')
        user_class_raw = fullNameDiv.find_element(By.TAG_NAME, 'span').text.split(" ")[2].strip("()")

        user_class = list(user_class_raw)
        user_class.insert(1, ".")

        return "".join(user_class)

    def getSeminars(self) -> list:
        # TODO: Find someone who has seminars and ask them for a copy of https://vyuka.gyarab.cz/seminare/
        delays = self.config.getDelays()
        self.browser.get(self.serverURL + "/seminare")
        time.sleep(delays[0])

        if "Pro Vaši skupinu nejsou momentálně k dispozici žádné semináře." in self.browser.page_source.encode().decode():
            return []
        else:
            return ["garbage data"]


    def convertGrades(self, grade: int|str):
        if type(grade) == str:
            match grade:
                case "A":
                    return 1
                case "B":
                    return 2
                case "C":
                    return 3
                case "D":
                    return 4
                case "F":
                    return 5
        else:
            match grade:
                case 1:
                    return "A"
                case 2:
                    return "B"
                case 3:
                    return "C"
                case 4:
                    return "D"
                case 5:
                    return "F"
    
    def processProgrammingAssignment(self, row: WebElement) -> dict:
        # FIXME: Handle unaccepted assignments and voluntary ones
        assignment = {}
        data = row.find_elements(By.TAG_NAME, 'td')
        i = 0

        while i < len(data):
            if i == 0:
                try:
                    values = data[i].find_element(By.TAG_NAME, 'a').text.split(": ")
                except NoSuchElementException:
                    values = data[i].text.split(": ")
                finally:
                    assignment.update({"name": ": ".join(values[1:])})
                    assignment.update({"type": values[0]})

            elif i == 1:
                assignment.update({"points": data[i].find_element(By.TAG_NAME, 'span').text})
            
            elif i == 2:
                try:
                    value = data[i].find_element(By.TAG_NAME, 'span')
                    assignment.update({
                        "accepted": True,
                        "date_accepted": value.text
                    })
                except NoSuchElementException:
                    accept_link = data[i].find_element(By.TAG_NAME, 'a')
                    assignment.update({
                        "accepted": False,
                        "date_accepted": None,
                        "accept_link": accept_link.get_attribute('href')
                    })
            
            elif i == 3:
                if data[i].text == "dobrovolné":
                    assignment.update({
                        "has_begun": False,
                        "date_begun": None,
                        "voluntary": True
                    })
                
                elif data[i].text == "nezahájeno":
                    assignment.update({
                        "has_begun": False,
                        "voluntary": False
                    })
                
                else:
                    value = data[i].find_element(By.TAG_NAME, 'span').text
                    assignment.update({
                        "has_begun": True,
                        "date_begun": value,
                        "voluntary": False
                    })
            elif i == 4:
                try:
                    value = data[i].find_element(By.TAG_NAME, 'span').text
                    assignment.update({"date_returned": value})
                except NoSuchElementException:
                    assignment.update({"date_returned": None})
            elif i == 5:
                try:
                    element = data[i].find_element(By.TAG_NAME, 'span')
                    assignment.update({"date_completed": element.text})
                except NoSuchElementException:
                    assignment.update({"date_completed": None})

            elif i == 6:
                try:
                    a_tag = data[i].find_element(By.TAG_NAME, 'a')
                    grade_data = a_tag.find_element(By.TAG_NAME, 'span').text.split(" ")

                    assignment.update({"grading": {
                        "total_points": grade_data[0],
                        "percentage": grade_data[1],
                        "final_mark": {
                            "cz": int(grade_data[2]),
                            "en": self.convertGrades(int(grade_data[2]))
                        }
                    }})
                except NoSuchElementException:
                    assignment.update({"grading": None})


            i += 1

        return assignment

    def getProgrammingAssignments(self, index: int) -> list:
        school_branch = self.getClass()[-1]
        delays = self.config.getDelays()

        if school_branch == "F":
            self.browser.get(self.serverURL + f"/kahoun/student/index.php?period={index}")
            time.sleep(delays[0])
            assignments = []
            table = self.browser.find_elements(By.TAG_NAME, "table")
            table_rows = table[0].find_elements(By.TAG_NAME, 'tbody')

            for row in table_rows:
                assignment_data = self.processProgrammingAssignment(row.find_element(By.TAG_NAME, 'tr'))
                assignments.append(assignment_data)

            return assignments
        else:
            return ["wrong branch!"]
        
    def getProgrammingAssignment(self, name: str) -> dict:
        # BUG: Fetching single programming sometimes doesn't return anything
        semester = Session.getCurrentSemester(Session.getSchoolYearByTime())
        assignments = self.getProgrammingAssignments(semester)

        for assign in assignments:
            if assign['name'] == name:
                return assign
            
        return {}
            
    def getProgrammingTotalGrade(self, index: int) -> dict:
        self.browser.get(self.serverURL + f"/kahoun/student/index.php?period={index}")
        table = self.browser.find_element(By.TAG_NAME, 'table')
        total_row = table.find_element(By.TAG_NAME, 'tfoot').find_element(By.TAG_NAME, 'tr').find_elements(By.TAG_NAME, 'th')
        data = {}

        i = 0
        while i < len(total_row):
            if i == 1:
                data.update({"total_available_points": total_row[i].find_element(By.TAG_NAME, 'span').text})
            
            if i == 3:
                text = total_row[i].find_element(By.TAG_NAME, 'span').find_element(By.TAG_NAME, 'span').text
                data.update({
                    "total_gotten_points": text.split()[0],
                    "average_percentage": text.split()[1],
                    "final_grade": text.split()[2]
                })

            i += 1

        return data