from collections import defaultdict
import concurrent.futures
import os
import re
import threading

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


thread_local = threading.local()
timeout = 8


def get_driver():
    if not (driver := getattr(thread_local, 'driver', None)):
        options = Options()
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        options.headless = True
        options.add_argument("--window-size=1440,422")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(executable_path=os.getcwd() + os.environ.get("CHROMEDRIVER_PATH"),
                                  options=options)
        setattr(thread_local, 'driver', driver)
    return driver


def get_element(element_xpath):
    driver = get_driver()
    try:
        element_present = ec.presence_of_element_located(
            (By.XPATH, element_xpath))
        return WebDriverWait(driver, timeout)\
            .until(element_present)
    except TimeoutException:
        return None


def get_elements(element_xpath):
    driver = get_driver()
    try:
        element_present = ec.presence_of_all_elements_located(
            (By.XPATH, element_xpath))
        return WebDriverWait(driver, timeout)\
            .until(element_present)
    except TimeoutException:
        return None


def get_company_timeslots(company_xpath):
    driver = get_driver()
    driver.get("https://app.careerfairplus.com/gt_ga/fair/2660/")

    # Select the specified company from the landing page.
    if not (company := get_element(company_xpath)):
        print("Timed out waiting for page to load.")
        return {}

    company_name = company.text
    if company_name.startswith("Featured Employer"):
        company_name = company.text.split("\n")[1]
    print(f"Finding timeslots for {company_name} with {driver}")
    company.click()

    # Wait for company landing page to load. If meetings are available, click the dropdown.
    meetings_xpath = "//*[@id='root']/div/div/div/div[3]/div/div[5]/div/div[1]/div[1]/div/div"
    if not (meetings := get_element(meetings_xpath)):
        print(f"{company_name} does not offer any meetings.")
        return {company_name: 0}
    meetings.click()

    # Retrieve recruiter list.
    recruiters_xpath = "//*[@id='root']/div/div/div/div[3]/div/div[5]/div/div[2]/div/div/div/ul/li"
    if not (recruiters := get_elements(recruiters_xpath)):
        print(f"No recruiters found for {company_name}.")
        return {}

    # Iterate through recruiters for a given company and track their available timeslots.
    num_slots = defaultdict(int)
    for recruiter in recruiters[1:]:
        try:
            timeslots = recruiter.find_element_by_xpath(".//div[1]/div/div/div[4]/div[1]")
            num_slots[company_name] += int(timeslots.get_attribute("innerText"))
        except NoSuchElementException:
            pass
        except ValueError:
            print(f"{company_name} has non-numeric timeslots.")
    return dict(num_slots)


def get_company_xpaths():
    url = "https://app.careerfairplus.com/gt_ga/fair/2660/"
    driver = get_driver()
    driver.get(url)
    num_companies_xpath = "//*[@id='root']/div/div/div/div[2]/li"
    if not (num_companies := get_element(num_companies_xpath)):
        print("Timed out waiting for page to load.")
        return []
    num_companies = int(re.findall('\d{3}', num_companies.text)[0])
    return [f"//*[@id='root']/div/div/div/div[2]/ul/div[{i}]"
            for i in range(2, num_companies + 2)]


def scrape():
    companies = get_company_xpaths()
    num_slots = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(os.environ.get("MAX_WORKERS"))) as executor:
        for result in executor.map(get_company_timeslots, companies):
            num_slots = {**num_slots, **result}
    get_driver().quit()
    return num_slots
