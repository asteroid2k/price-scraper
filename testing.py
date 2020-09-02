from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
chromedriver_path = "./chromedriver.exe"

driver = webdriver.Chrome(chromedriver_path)

driver.get('https://www.kikuu.com/')
searchbar = driver.find_element_by_xpath("//input[@class='search-input']")
searchbar.send_keys("laptop stickers")
searchbar.send_keys(Keys.RETURN)
try:
    search_list = driver.find_element(By.CLASS_NAME, "searchGoods")
    products = search_list.find_elements_by_tag_name("li")
    i = 1
    for product in products:
        p_link = product.find_element(By.TAG_NAME, "a")
        p_content = p_link.find_element(By.CLASS_NAME,  "searchGoods-content")
        print(f"{i}-", end='')
        print(p_content.find_element_by_class_name("searchGoods-name").text)
        i += 1

finally:
    driver.quit()
