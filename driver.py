from selenium import webdriver
import jumia_scraper
import kikuu_scraper
import pandas as pd


def main(search_str, pages, site):
    chromedriver_path = "./chromedriver.exe"
    # Instantiate a headless chrome webdriver so chrome window does not open
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-gpu")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(chromedriver_path, options=options)

    if site.lower() == "kikuu":
        return kikuu_scraper.scrape(webdriver=driver, search_input=search_str, search_page_limit=pages)
    elif site.lower() == "jumia":
        return jumia_scraper.scrape(webdriver=driver, search_input=search_str, search_page_limit=pages)
    else:
        return "", True, "Sites do not match any"


def filter_results(filename, qfilter, value, param, info):
    err = False
    err_msg = ""
    dataframe = {}

    info["param"] = param
    info["value"] = value
    info["op"] = qfilter

    if not filename:
        err = True
        err_msg = "No Data"
        return err, err_msg, {}, {}

    try:
        dataframe = pd.read_csv(filename)
        info["currency"], _ = dataframe["Price"][0].split(" ")
        # remove currency and commas from price and convert to float for computation
        dataframe["Price"] = dataframe["Price"].apply(
            lambda x: float(x.replace(",", "").split(" ")[1]))
        # convert rating and number of reviews to float
        dataframe["Rating"] = dataframe["Rating"].apply(
            lambda x: float(x))
        dataframe["Reviews"] = dataframe["Reviews"].apply(
            lambda x: float(x))
        # create new column with reviews x rating
        dataframe['Weight'] = dataframe.apply(
            lambda row: row.Rating * row.Reviews, axis=1)
        # get most and least popular items
        max_rev = dataframe.query("Weight==Weight.max()").head(1)
        min_rev = dataframe.query("Weight==Weight.min()").head(1)
        # get most and expensive popular items
        low = dataframe.query("Price==Price.min()").head(1)
        high = dataframe.query("Price==Price.max()").head(1)
        # gather necessary metrics
        info["avg"] = dataframe["Price"].mean().round(2)
        info["total"] = dataframe.shape[0]
        info["high"] = high["Price"].iloc[0]
        info["low"] = low["Price"].iloc[0]
        # gather item links
        info["max_rev_item"] = max_rev["Link"].iloc[0]
        info["min_rev_item"] = min_rev["Link"].iloc[0]
        info["high_item"] = high["Link"].iloc[0]
        info["low_item"] = low["Link"].iloc[0]
        dataframe = dataframe.round(2)

    except Exception as e:
        err = True
        err_msg = e

    if err:
        print(f"ERROR:{err_msg}")
        return err, err_msg, {}, {}

    if qfilter and param:
        if param == "price":
            dataframe.query(f"Price {qfilter} {value} ", inplace=True)
            return err, err_msg, dataframe, info
        elif param == "rating":
            dataframe.query(f"Rating {qfilter} {value} ", inplace=True)
            return err, err_msg, dataframe, info
        elif param == "reviews":
            dataframe.query(f"Reviews {qfilter} {value} ", inplace=True)
            return err, err_msg, dataframe, info
    else:
        return err, err_msg, dataframe, info


if __name__ == "__main__":
    # test
    print(main("hello", 1, "kikuu"))
