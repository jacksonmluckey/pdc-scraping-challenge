import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def get_a_tags(driver, class_="titolo"):
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    a_tags = soup.find_all("a", class_=class_)
    return a_tags


def print_page_data(driver):
    a_tags = get_a_tags(driver)
    for a_tag in a_tags:
        data = parse_a_tag(a_tag)
        print(data)
    return 0


def parse_a_tag(a_tag):
    return (a_tag["href"], a_tag.text)


if __name__ == "__main__":

    # Initiate browser, navigate to page and wait for JS to load properly
    options = webdriver.FirefoxOptions()
    options.binary_location = "~/Downloads/geckodriver"
    driver = webdriver.Firefox()
    driver.get("https://www.quirinale.it/ricerca/comunicati")
    time.sleep(5)
    print_page_data(driver)

    for i in range(1, 10):
        pagination = driver.find_elements(By.CLASS_NAME, "js-paginatore")
        pagination[i - 1].click()
        time.sleep(5)
        print_page_data(driver)

    driver.close()
