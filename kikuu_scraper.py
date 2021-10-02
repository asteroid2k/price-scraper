# Import selenium
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, WebDriverException
import csv
import time


def scrape(webdriver=None, search_input="", search_page_limit=0):
    if webdriver is None:
        return "", True, "No Web Driver"

    source = "https://www.kikuu.com.gh/"
    error_msg, error = "", False
    # csv file initialization
    csv_filename = search_input.replace(" ", "_")+"-kikuu.csv"
    headers = ["Name", "Price", "Rating", "Reviews", "Link"]
    # open csv file and wirte column headers
    with open(csv_filename, mode='w') as file:
        writer = csv.writer(file, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(headers)
    webdriver.implicitly_wait(5)

    webdriver.get(source)
    time.sleep(5)

    # find search bar and input search string
    searchbar = webdriver.find_element_by_xpath(
        "//input[@class='search-input']")
    searchbar.send_keys(search_input)
    searchbar.send_keys(Keys.RETURN)
    time.sleep(5)

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
                try:
                    product = p.find_element(By.TAG_NAME, "a")
                    p_link = product.get_attribute("href")
                    p_content = product.find_element(
                        By.CLASS_NAME,  "searchGoods-content")
                    p_name = p_content.find_element_by_class_name(
                        "searchGoods-name").text
                    p_price = p_content.find_element_by_class_name(
                        "searchGoods-price").text

                    # get reviews if available
                    rev = ""
                    p_stars = ""
                    p_reviews = ""
                    p_r = ""
                    try:
                        rev = p_content.find_element_by_class_name(
                            "searchGoods-other")
                    except Exception:
                        pass
                    if rev:
                        # get number of reviews
                        p_r = rev.find_element_by_class_name(
                            "searchGoods-other-orders").text
                        p_reviews = p_r.split(" ")[0]
                        # get total stars/rating
                        p_stars = rev.find_element_by_class_name(
                            "stars").text
                    # write product details in csv file
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
            i += 1
            if i <= search_page_limit:
                # find and click on next page icon
                next_page_button = pagination.find_element_by_class_name(
                    "nextBox")
                next_page_button = next_page_button.find_element_by_tag_name(
                    "i")
                next_page_button.click()
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
        print(f"ERROR: {error_msg}")
    return csv_filename, error, error_msg


if __name__ == "__main__":
    # test
    scrape(search_input="asdf", search_page_limit=1)
