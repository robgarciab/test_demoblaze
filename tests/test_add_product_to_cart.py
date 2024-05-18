import os

from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
import pytest

base = 'a.blazemeter.com'
API_KEY = os.getenv('BZM_API_KEY')
API_SECRET = os.getenv('BZM_API_SECRET')
blazegrid_url = 'https://{}:{}@{}/api/v4/grid/wd/hub'.format(API_KEY, API_SECRET, base)

bzm_options = {
    'blazemeter.sessionName': 'My Test Session',
    'blazemeter.videoEnabled': 'True',
    'blazemeter.testId': os.getenv('BZM_TEST_ID')
}
browser_options = webdriver.FirefoxOptions()
browser_options.browser_version = 'default'
browser_options.set_capability('bzm:options', bzm_options)

args = {
    'testSuiteName': 'Add Product to Cart'
}


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Remote(command_executor=blazegrid_url, options=browser_options)
    driver.implicitly_wait(30)
    yield driver
    driver.quit()


def handle_alert(driver):
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        return alert_text
    except NoAlertPresentException:
        return None


def test_add_product_to_cart(driver):
    base_url = "https://demoblaze.com"

    # Label: Home
    args['testCaseName'] = 'Home'
    driver.execute_script("/* FLOW_MARKER test-case-start */", args)
    driver.get(f"{base_url}/index.html")
    args['status'] = 'passed'
    args['message'] = 'Home page loaded successfully'
    driver.execute_script("/* FLOW_MARKER test-case-stop */", args)

    # Label: Phones
    args['testCaseName'] = 'Phones'
    driver.execute_script("/* FLOW_MARKER test-case-start */", args)
    driver.find_element(By.XPATH, "//*[text() = 'Phones']").click()
    args['status'] = 'passed'
    args['message'] = 'Phones page loaded successfully'
    driver.execute_script("/* FLOW_MARKER test-case-stop */", args)

    # Label: View Product
    args['testCaseName'] = 'View product'
    driver.execute_script("/* FLOW_MARKER test-case-start */", args)
    driver.find_element(By.CSS_SELECTOR, "img.card-img-top.img-fluid").click()
    args['status'] = 'passed'
    args['message'] = 'Product page loaded successfully'
    driver.execute_script("/* FLOW_MARKER test-case-stop */", args)

    # Label: Add product to cart
    args['testCaseName'] = 'Add product to cart'
    driver.execute_script("/* FLOW_MARKER test-case-start */", args)
    driver.find_element(By.XPATH, "//*[text() = 'Add to cart']").click()
    args['status'] = 'passed'
    args['message'] = 'Product added successfully'
    driver.execute_script("/* FLOW_MARKER test-case-stop */", args)

    # Handle product added to cart alert
    handle_alert(driver)

    # Label: View cart
    args['testCaseName'] = 'View cart'
    del args['status']
    del args['message']
    driver.execute_script("/* FLOW_MARKER test-case-start */", args)
    driver.find_element(By.XPATH, "//*[text() = 'Cart']").click()
    args['status'] = 'passed'
    args['message'] = 'Cart page loaded successfully'
    driver.execute_script("/* FLOW_MARKER test-case-stop */", args)
