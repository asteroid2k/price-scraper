from selenium import webdriver
import jumia_scraper
import kikuu_scraper
import pandas as pd


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


def filter_results(filename, qfilter, value, info):
    err = False
    err_msg = ""
    dataframe = {}
    try:
        dataframe = pd.read_csv(filename)
        currency, _ = dataframe["Price"][0].split(" ")
        dataframe["Price"] = dataframe["Price"].apply(lambda x: float(x[4:]))
        info["max"] = dataframe["Price"].max()
        info["min"] = dataframe["Price"].min()
        info["avg"] = dataframe["Price"].mean()

    except Exception as e:
        err = True
        err_msg = e

    if err:
        return err, err_msg, {}, {}

    if qfilter.lower() == "eq":
        dataframe.query(f"Price == {value} ", inplace=True)
        dataframe.rename(
            columns={"Price": f"Price ({currency})"}, inplace=True)
        return err, err_msg, dataframe, info
    else:
        dataframe.rename(
            columns={"Price": f"Price ({currency})"}, inplace=True)
        return err, err_msg, dataframe, info


if __name__ == "__main__":
    # test
    print(main("hello", 1, "kikuu"))
