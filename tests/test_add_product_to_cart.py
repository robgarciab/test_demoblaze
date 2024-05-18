import os

from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException
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
    try:
        driver.get(f"{base_url}/index.html")
        args['status'] = 'passed'
        args['message'] = 'Home page loaded successfully'
    except NoSuchElementException:
        args['status'] = 'broken'
        args['message'] = "Home page didn't load"
    driver.execute_script("/* FLOW_MARKER test-case-stop */", args)

    # Label: Phones
    args['testCaseName'] = 'Phones'
    driver.execute_script("/* FLOW_MARKER test-case-start */", args)
    try:
        driver.find_element(By.XPATH, "//*[text() = 'Phones']").click()
        args['status'] = 'passed'
        args['message'] = 'Phones page loaded successfully'
    except NoSuchElementException:
        args['status'] = 'broken'
        args['message'] = 'Phones element not found'
    driver.execute_script("/* FLOW_MARKER test-case-stop */", args)

    # Label: View Product
    args['testCaseName'] = 'View product'
    driver.execute_script("/* FLOW_MARKER test-case-start */", args)
    try:
        driver.find_element(By.CSS_SELECTOR, "img.card-img-top.img-fluid").click()
        args['status'] = 'passed'
        args['message'] = 'Product page loaded successfully'
    except NoSuchElementException:
        args['status'] = 'broken'
        args['message'] = 'Product element not found'
    driver.execute_script("/* FLOW_MARKER test-case-stop */", args)

    # Label: Add product to cart
    args['testCaseName'] = 'Add product to cart'
    driver.execute_script("/* FLOW_MARKER test-case-start */", args)
    try:
        driver.find_element(By.XPATH, "//*[text() = 'Add to cart']").click()
        # Handle product added to cart alert
        handle_alert(driver)
        args['status'] = 'passed'
        args['message'] = 'Product added successfully'
    except NoSuchElementException:
        args['status'] = 'broken'
        args['message'] = 'Add to cart element not found'
    driver.execute_script("/* FLOW_MARKER test-case-stop */", args)

    # Label: View cart
    args['testCaseName'] = 'View cart'
    driver.execute_script("/* FLOW_MARKER test-case-start */", args)
    try:
        driver.find_element(By.XPATH, "//*[text() = 'Cart']").click()
        args['status'] = 'passed'
        args['message'] = 'Cart page loaded successfully'
    except NoSuchElementException:
        args['status'] = 'broken'
        args['message'] = 'Cart element not found'
    driver.execute_script("/* FLOW_MARKER test-case-stop */", args)
