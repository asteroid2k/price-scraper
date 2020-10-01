# Import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
# Import csv module
import csv
import time
from datetime import datetime


def scrape(webdriver=None, search_input="", search_page_limit=0):
    if webdriver is None:
        return "", True, "No Web Driver"

    source = "https://www.kikuu.com/"
    error_msg, error = "", False
    csv_filename = f"{search_input}-kikuu.csv"
    headers = ["Name", "Price", "Link"]

    with open(csv_filename, mode='w') as file:
        writer = csv.writer(file, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)

    webdriver.get(source)
    # find search bar and input search string
    searchbar = webdriver.find_element_by_xpath(
        "//input[@class='search-input']")
    searchbar.send_keys(search_input)
    searchbar.send_keys(Keys.RETURN)
    i = 1
    while i <= search_page_limit:

        try:
            # raise exception if there are no search results
            if webdriver.find_elements_by_class_name("searchEmpty"):
                error_msg = "No Search Results"
                raise WebDriverException

            # wait for search results to load(timeout 10secs)
            search_list = WebDriverWait(webdriver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "searchGoods")))
            pagination = WebDriverWait(webdriver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "store-pagination")))
            pages = pagination.find_elements_by_class_name("pageItem")

            # get list of searched products
            products = search_list.find_elements_by_tag_name("li")
            on_page = pagination.find_element_by_css_selector(
                ".pageItem.active")
            print(f"\nPage {on_page.text}/{pages[-1].text}")

            # go through each product in search results and extract info
            for p in products:
                product = p.find_element(By.TAG_NAME, "a")
                p_link = product.get_attribute("href")
                p_content = product.find_element(
                    By.CLASS_NAME,  "searchGoods-content")
                p_name = p_content.find_element_by_class_name(
                    "searchGoods-name").text
                p_price = p_content.find_element_by_class_name(
                    "searchGoods-price").text
                with open(csv_filename, mode='a', encoding='utf-8') as file:
                    csv_writer = csv.writer(
                        file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    csv_writer.writerow([p_name, p_price, p_link])
                # print(f"({j}){p_name[:20]} - {p_price}")
                # print(f"->{p_link}")

            # find and click on next page icon
            next_page_button = pagination.find_element_by_class_name("nextBox")
            next_page_button = next_page_button.find_element_by_tag_name("i")
            next_page_button.click()
            time.sleep(2)
            i += 1

        except TimeoutException:
            error = True
            error_msg = "Timeout error: Check internet connection."
            break
        except WebDriverException:
            error = True
            break

    webdriver.quit()
    return csv_filename, error, error_msg


if __name__ == "__main__":

    scrape(search_input="asdf", search_page_limit=1)
