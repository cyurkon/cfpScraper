from collections import defaultdict
import concurrent.futures
import time
import threading

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


thread_local = threading.local()
# values = defaultdict(dict)


def scrape():
    url = "https://app.careerfairplus.com/gt_ga/fair/2660/"
    driver = get_driver()
    driver.get(url)
    time.sleep(3)
    return driver.find_elements_by_css_selector("div[style='cursor: pointer;']")


def get_driver():
    driver = getattr(thread_local, 'driver', None)
    if not driver:
        print("Creating new driver")
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1440,422")
        driver = webdriver.Chrome(options=options)
        setattr(thread_local, 'driver', driver)
    print(f"Returning driver {driver}")
    return driver


def get_timeslots(company):
    driver = get_driver()
    print(company.text)
    print(company.parent)
    # print(f"Finding timeslots for {company.text} with {driver}")
    company.click()
    time.sleep(2)
    print(f"I'm awake again with {driver}")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    print(soup)
    employer_card = soup.find("div", {"class": "desktop-employer-card-container"})
    title = employer_card.find("div", {"class": "employer-card-title"})
    print(title.text)
    try:
        meetings = driver.find_element_by_xpath("//*[@id='root']/div/div/div/div[3]/div/div[5]/div/div[1]/div["
                                                "1]/div/div")
        meetings.click()
    except NoSuchElementException:
        pass
    time.sleep(2)
    recruiters = driver.find_elements_by_xpath("//*[@id='root']/div/div/div/div[3]/div/div[5]/div/div["
                                               "2]/div/div/div/ul/li")
    values = defaultdict(dict)
    for recruiter in recruiters:
        try:
            name = recruiter.find_element_by_xpath(".//div[1]/div/div/div[2]/div[2]/h6")
            timeslots = recruiter.find_element_by_xpath(".//div[1]/div/div/div[4]/div[1]")
            values[company.text][name.text] = timeslots.text
        except NoSuchElementException:
            pass
    return values


if __name__ == "__main__":
    companies = scrape()
    print(f"Companies to scrape: {', '.join([company.text for company in companies])}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(get_timeslots, companies)
        for future in concurrent.futures.as_completed(results):
            print(future.result())
        # return {company: results for company}
    # print(values)
