from collections import defaultdict
from multiprocessing.pool import ThreadPool
import time
import threading

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

url = "https://app.careerfairplus.com/gt_ga/fair/2660/"
options = Options()
options.headless = True
options.add_argument("--window-size=1440,422")
values = defaultdict(dict)

with webdriver.Chrome(options=options) as driver:
    driver.get(url)
    time.sleep(1)
    companies = driver.find_elements_by_css_selector("div[style='cursor: pointer;']")
    for company in companies:
        company.click()
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        employer_card = soup.find("div", {"class": "desktop-employer-card-container"})
        title = employer_card.find("div", {"class": "employer-card-title"})
        print(title.text)
        try:
            meetings = driver.find_element_by_xpath("//*[@id='root']/div/div/div/div[3]/div/div[5]/div/div[1]/div["
                                                    "1]/div/div")
            meetings.click()
        except NoSuchElementException as e:
            continue
        time.sleep(1)
        recruiters = driver.find_elements_by_xpath("//*[@id='root']/div/div/div/div[3]/div/div[5]/div/div["
                                                   "2]/div/div/div/ul/li")
        for recruiter in recruiters:
            try:
                name = recruiter.find_element_by_xpath(".//div[1]/div/div/div[2]/div[2]/h6")
                timeslots = recruiter.find_element_by_xpath(".//div[1]/div/div/div[4]/div[1]")
                values[company.text][name.text] = timeslots.text
            except NoSuchElementException as e:
                pass
print(values)
