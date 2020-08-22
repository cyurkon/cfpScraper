from collections import defaultdict
import concurrent.futures
import re
import threading
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


thread_local = threading.local()


def get_driver():
    driver = getattr(thread_local, 'driver', None)
    if not driver:
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1440,422")
        driver = webdriver.Chrome(options=options)
        setattr(thread_local, 'driver', driver)
    return driver


def get_timeslots(company_xpath):
    driver = get_driver()
    driver.get("https://app.careerfairplus.com/gt_ga/fair/2660/")
    time.sleep(2)
    company = driver.find_element_by_xpath(company_xpath)
    print(f"Finding timeslots for {company.text} with {driver}")
    company.click()
    time.sleep(2)
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
    return dict(values)


def get_company_xpaths():
    url = "https://app.careerfairplus.com/gt_ga/fair/2660/"
    driver = get_driver()
    driver.get(url)
    time.sleep(2)
    num_companies_text = driver.find_element_by_xpath("//*[@id='root']/div/div/div/div[2]/li").text
    num_companies = int(re.findall('\d{3}', num_companies_text)[0])
    # return [f"//*[@id='root']/div/div/div/div[2]/ul/div[{i}]"
    #         for i in range(2, 6)]
    return [f"//*[@id='root']/div/div/div/div[2]/ul/div[{i}]"
            for i in range(2, num_companies + 2)]


if __name__ == "__main__":
    companies = get_company_xpaths()
    available_timeslots = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for result in executor.map(get_timeslots, companies):
            available_timeslots = {**available_timeslots, **result}
    get_driver().quit()
    print(len(available_timeslots))
