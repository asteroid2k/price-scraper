from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options

chromedriver_path = "./chromedriver.exe"

options = webdriver.ChromeOptions()
options.headless = True

driver = webdriver.Chrome(chromedriver_path, options=options)

search_input = "Iphone X cases"
search_page_limit = 2

driver.get('https://www.kikuu.com/')
searchbar = driver.find_element_by_xpath("//input[@class='search-input']")
searchbar.send_keys(search_input)
searchbar.send_keys(Keys.RETURN)
i, j = 1, 1
while i <= search_page_limit:

    try:
        if driver.find_elements_by_class_name("searchEmpty"):
            print('No Search Results')
            raise WebDriverException

        search_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "searchGoods")))
        pagination = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "store-pagination")))
        pages = pagination.find_elements_by_class_name("pageItem")
        products = search_list.find_elements_by_tag_name("li")
        on_page = pagination.find_element_by_css_selector(".pageItem.active")
        print(f"\nPage {on_page.text}/{pages[-1].text}")

        for p in products[:5]:
            product = p.find_element(By.TAG_NAME, "a")
            p_link = product.get_attribute("href")
            p_content = product.find_element(
                By.CLASS_NAME,  "searchGoods-content")
            p_name = p_content.find_element_by_class_name(
                "searchGoods-name").text
            p_price = p_content.find_element_by_class_name(
                "searchGoods-price").text
            print(f"({j}){p_name[:20]} - {p_price}")
            print(f"->{p_link}")
            j += 1

        next_page_button = pagination.find_element_by_class_name("nextBox")
        next_page_button = next_page_button.find_element_by_tag_name("i")
        next_page_button.click()
        i += 1

    except (TimeoutException, WebDriverException) as e:
        print(e)
        break
    # if i > search_page_limit:
    #     break
driver.quit()
