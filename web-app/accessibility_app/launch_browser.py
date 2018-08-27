from selenium import webdriver


def launch_browser(browser, url):
    driver = webdriver.Chrome()
    if (url.startswith('http://') or url.startswith('https://')):
        driver.get(url)
    else:
        driver.get('http://' + url)
