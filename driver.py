from selenium import webdriver
import jumia_scraper
import kikuu_scraper


def main(search_str, pages, site):
    chromedriver_path = "./chromedriver.exe"
    # Instantiate a headless chrome webdriver so chrome window does not open
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(chromedriver_path, options=options)

    if site.lower() == "kikuu":
        return kikuu_scraper.scrape(webdriver=driver, search_input=search_str, search_page_limit=pages)
    elif site.lower() == "jumia":
        return jumia_scraper.scrape(webdriver=driver, search_input=search_str, search_page_limit=pages)
    else:
        return "", True, "Sites do not match any"


if __name__ == "__main__":
    # test
    print(main("hello", 1, "kikuu"))
