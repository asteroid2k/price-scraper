# Import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
# Import csv module
import csv
import time
import datetime


chromedriver_path = "./chromedriver.exe"
# Instantiate a headless chrome webdriver so chrome window does not open
options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(chromedriver_path)

source = 'https://www.jumia.com.gh/'
search_input = "Iphone X cases"
search_page_limit = 2
csv_filename = f"{search_input}{datetime.date.today()}.csv"
csv_filename = csv_filename.replace(' ', '_')
headers = ["No", "Name", "Price", "Link"]

with open(csv_filename, mode='w') as file:
    writer = csv.writer(file, delimiter=',',
                        quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(headers)
driver.get(source)

# find search bar and input search string
searchbar = driver.find_element_by_xpath("//input[@id='fi-q']")
searchbar.send_keys(search_input)
searchbar.send_keys(Keys.RETURN)

i, j = 1, 1
while i <= search_page_limit:

    try:
        # raise exception if there are no search results
        if driver.find_elements_by_css_selector(".-pvs.-fs16.-m"):
            print('No Search Results')
            raise WebDriverException

        # wait for search results to load(timeout 10secs)
        search_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".-paxs.row._no-g._4cl-3cm-shs")))
        pagination = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".pg-w.-pvxl")))
        active_page = pagination.find_element_by_css_selector(".pg._act")

        # get list of searched products
        products = search_list.find_elements_by_tag_name("article")

        print(f"\nPage {active_page.text}")

        # go throught each product in search results and extract info
        for p in products:
            product = p.find_element(By.TAG_NAME, "a")
            p_link = product.get_attribute("href")
            p_content = product.find_element(
                By.CLASS_NAME,  "info")
            p_name = p_content.find_element_by_class_name(
                "name").text
            p_price = p_content.find_element_by_class_name(
                "prc").text
            with open(csv_filename, mode='a', encoding='utf-8') as file:
                csv_writer = csv.writer(
                    file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow([j, p_name, p_price, p_link])
            print(f"({j}){p_name[:20]} - {p_price}")
            print(f"->{p_link}")
            j += 1

        # find and click on next page icon
        i += 1

        driver.get(driver.current_url+f"&page={i}")
        # next_page_button = pagination.find_elements_by_class_name("pg")[-2]
        # next_page_button = next_page_button.find_element_by_class_name("ic")
        # next_page_button.click()
        time.sleep(2)

    except (TimeoutException, WebDriverException) as e:
        print("An error occured", e)
        break

driver.quit()
