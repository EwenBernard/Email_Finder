import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests
import time

@pytest.fixture
def browser():
    # Set up the WebDriver
    driver = webdriver.Chrome()  # You can use other drivers like Firefox or Edge as well
    yield driver
    # Teardown: Close the WebDriver
    driver.quit()

def test_form_submission(browser):
    # Open the website
    print("IN FORM")
    browser.get("http://127.0.0.1:8001/")

    # Find and fill in the form
    name_input = browser.find_element(By.ID,"name")
    last_name_input = browser.find_element(By.ID,"lastName")
    company_input = browser.find_element(By.ID,"company")

    name_input.send_keys("Pascal")
    last_name_input.send_keys("Sager")
    company_input.send_keys("efrei.fr")

    # Submit the form
    search_button = browser.find_element(By.CLASS_NAME, "search-button")
    search_button.click()

    time.sleep(10)

    # Wait for the result container to appear
    result_container = browser.find_element(By.ID, "resultContainer")
    assert "show" in result_container.get_attribute("class")

    #Check matched email
    contact_info = browser.find_element(By.CLASS_NAME,"contact-info")
    assert contact_info.find_element(By.XPATH, "//p[contains(text(),'Pascal Sager')]")
    assert contact_info.find_element(By.XPATH, "//p[contains(text(),'EFREI, Paris-Panthéon-Assas University')]")

    confidence_tag = browser.find_element(By.CLASS_NAME,"confidence-tag")
    assert confidence_tag.find_element(By.XPATH, "//span[contains(@class, 'tag--success')]/b[contains(text(),'99%')]")

    #Check source list
    source_list = browser.find_element(By.CLASS_NAME,"source-list")
    assert source_list.find_element(By.XPATH, "//li[contains(text(),'efrei.fr')]")

    #Check related source list
    related_results = browser.find_element(By.CLASS_NAME, "result-list-container")
    assert related_results.find_element(By.XPATH, "//p[contains(@class,'result-list-title') and contains(text(),'Other Related Results')]")
    assert related_results.find_element(By.XPATH, "//ul/li")

def test_post_request():
    # Check the status code and content of the POST request
    response = requests.post("http://127.0.0.1:8001/add", data={
        "name": "Pascal",
        "last_name": "Sager",
        "company_name": "efrei.fr"
    })

    assert response.status_code == 200

    response_data = response.json()
    assert "matched_result" in response_data
    assert "remaining_data" in response_data
    

if __name__ == "__main__":
    pytest.main()