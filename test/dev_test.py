from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests

browser = webdriver.Chrome()

browser.get("http://127.0.0.1:8001/")

# Find and fill in the form
name_input = browser.find_element(By.ID,"name")
last_name_input = browser.find_element(By.ID,"lastName")
company_input = browser.find_element(By.ID,"company")

name_input.send_keys("John")
last_name_input.send_keys("Doe")
company_input.send_keys("ABC Corp")

# Submit the form
search_button = browser.find_element(By.CLASS_NAME, "search-button")
search_button.click()

time.sleep(3)

contact_info = browser.find_element(By.CLASS_NAME,"contact-info")
print(contact_info.find_element(By.XPATH, "//p[contains(text(),'John Doe')]"))
print(contact_info.find_element(By.XPATH, "//p[contains(text(),'ABC Corp')]"))

confidence_tag = browser.find_element(By.CLASS_NAME,"confidence-tag")
print(confidence_tag.find_element(By.XPATH, "//span[contains(@class, 'tag--success')]/b[contains(text(),'97%')]"))

#Check source list
source_list = browser.find_element(By.CLASS_NAME,"source-list")
print(source_list.find_element(By.XPATH, "//li[contains(text(),'Source 1')]"))

#Check related source list
related_results = browser.find_element(By.CLASS_NAME, "result-list-container")
print(related_results.find_element(By.XPATH, "//p[contains(@class,'result-list-title') and contains(text(),'Other Related Results')]"))
print(related_results.find_element(By.XPATH, "//ul/li"))


browser.quit()