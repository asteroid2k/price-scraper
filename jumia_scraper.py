# Import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
# Import csv module
import csv
import time
import re


def scrape(webdriver=None, search_input="", search_page_limit=0):

    if webdriver is None:
        return "", True, "No Web Driver"

    error_msg, error = "", False
    source = 'https://www.jumia.com.gh/'
    # csv file initialization
    csv_filename = search_input.replace(" ", "_")+"-jumia.csv"
    headers = ["Name", "Price", "Rating", "Reviews", "Link"]
    # open csv file and wirte column headers
    with open(csv_filename, mode='w') as file:
        writer = csv.writer(file, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
    webdriver.implicitly_wait(5)
    webdriver.get(source)
    time.sleep(5)
    # webdriver.get_screenshot_as_file("screenshot.png")

    # find search bar and input search string
    searchbar = webdriver.find_element_by_xpath("//input[@id='fi-q']")
    searchbar.send_keys(search_input)
    searchbar.send_keys(Keys.RETURN)
    time.sleep(5)

    i = 1
    while i <= search_page_limit:

        try:
            # raise exception if there are no search results
            if webdriver.find_elements_by_css_selector(".-pvs.-fs16.-m"):
                error_msg = "No Search Results"
                raise WebDriverException

            # wait for search results to load(timeout 10secs)
            search_list = WebDriverWait(webdriver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".-paxs.row._no-g._4cl-3cm-shs")))
            try:
                pagination = webdriver.find_element(
                    By.CSS_SELECTOR, ".pg-w.-pvxl")
                active_page = pagination.find_element_by_css_selector(
                    ".pg._act").text
            except NoSuchElementException:
                active_page = 1

            # get list of searched products
            products = search_list.find_elements_by_tag_name("article")

            print(f"\nPage {active_page}")

            # go through each product in search results and extract info
            for p in products:
                try:
                    product = p.find_element(By.TAG_NAME, "a")
                    p_link = product.get_attribute("href")
                    p_content = product.find_element(
                        By.CLASS_NAME,  "info")
                    p_name = p_content.find_element_by_class_name(
                        "name").text
                    p_price = p_content.find_element_by_class_name(
                        "prc").text

                    # get reviews if available
                    rev = ""
                    try:
                        rev = p_content.find_element_by_class_name("rev").text
                    except Exception:
                        pass
                    p_stars = 0
                    p_reviews = 0
                    if rev:
                        # get total review e.g '5' out of 5. we need just the first number
                        p_stars = rev.split(" ")[0]
                        # get number of reviews. e.g (8). so use regex to get number out of parenthesis
                        m = re.search(r"\((\w+)\)", rev)
                        p_reviews = m.group(1)
                    # continue if element is not present
                    with open(csv_filename, mode='a', encoding='utf-8') as file:
                        csv_writer = csv.writer(
                            file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        csv_writer.writerow(
                            [p_name, p_price, p_stars, p_reviews, p_link])
                # continue if element is not present
                except StaleElementReferenceException:
                    continue
                except Exception as e:
                    error_msg = e

            # go to next page
            i += 1
            if i <= search_page_limit:
                webdriver.get(webdriver.current_url+f"&page={i}")
                time.sleep(5)

        except TimeoutException:
            error = True
            error_msg = "Timeout error: Check internet connection."
            break
        except WebDriverException:
            error = True
            break

    webdriver.quit()
    if error:
        print(f"ERROR:{error_msg}")
    return csv_filename, error, error_msg


if __name__ == "__main__":

    scrape(search_input="asdf", search_page_limit=1)
