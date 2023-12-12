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

    time.sleep(3)

    assert browser.find_element(By.CLASS_NAME, "result-container")
    assert browser.find_element(By.XPATH, '//*[@id="resultContainer"]/div[1]/div[1]/div[2]/p[1]')
    assert browser.find_element(By.XPATH, '//*[@id="resultContainer"]/div[1]/div[1]/div[2]/p[2]')
   
    #Check source list
    assert browser.find_element(By.CLASS_NAME,"source-list")

    assert browser.find_element(By.XPATH, '//*[@id="resultContainer"]/div[2]/p')
    assert browser.find_element(By.XPATH, '//*[@id="resultContainer"]/div[2]/ul/li[1]/div/div[2]/p[1]')

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