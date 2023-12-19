from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


service = Service(executable_path="./chromedriver");
driver = webdriver.Chrome(service=service);

driver.get("https://aguasdejoinville.com.br/sansys/index.html#/");

WebDriverWait(driver, 5) \
    .until(EC.presence_of_element_located((By.CLASS_NAME, "q-field__native.q-placeholder")));

name_input = driver.find_element(By.CSS_SELECTOR, ".q-field__native.q-placeholder[name='username']");
password_input = driver.find_element(By.CSS_SELECTOR, ".q-field__native.q-placeholder[name='password']");
submit_login = driver.find_element(By.CSS_SELECTOR, "[name='btn_logar']");

name_input.clear();
password_input.clear();

name_input.send_keys("vogel.000001");
password_input.send_keys("Caj323");
submit_login.click();
time.sleep(2);
submit_login.click();


# WebDriverWait(driver, 20) \
#     .until(EC.presence_of_element_located((By.CSS_SELECTOR, ".q-icon.notranslate.material-icons")))
driver.find_element(By.CSS_SELECTOR, "[name=menuItem']").click();

time.sleep(10);

driver.quit();
