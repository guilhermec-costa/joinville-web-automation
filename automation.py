from selenium import webdriver;
from selenium.webdriver.chrome.service import Service;
from selenium.webdriver.common.by import By;
from selenium.webdriver.common.keys import Keys;
from utils import get_element_after_rendered, finish_os;
import pandas as pd
import numpy as np

import time

data = pd.read_excel("./data.xlsx");
rgis = data["rgi"].unique();


service = Service(executable_path=r"./chromedriver");
driver = webdriver.Chrome(service=service);

driver.get("https://aguasdejoinville.com.br/sansys/index.html");
driver.maximize_window();

time.sleep(2);

name_input = driver.find_element(By.CSS_SELECTOR, ".q-field__native.q-placeholder[name='username']");
password_input = driver.find_element(By.CSS_SELECTOR, ".q-field__native.q-placeholder[name='password']");
submit_login = driver.find_element(By.CSS_SELECTOR, "[name='btn_logar']");

name_input.clear();
password_input.clear();

# login form
name_input.send_keys("vogel.000001");
password_input.send_keys("Caj323");
submit_login.click();
time.sleep(0.3);
submit_login.click();
OS_STATUS_POSITION_IN_TABLE = 3;
menu_item = get_element_after_rendered(driver, elem_name="button[name='menuItem']",)

for i, rgi in enumerate(rgis):
    menu_item.click();
    # from the first iteration, the link will be already open. No need to expand it again
    if i == 0:
        attendence_button = get_element_after_rendered(driver, elem_name="div[name='M00003']",)
        attendence_button.click();

    time.sleep(0.7);
    start_attendence_link = get_element_after_rendered(driver, elem_name="a[href='#/interno/atendimento']")
    start_attendence_link.click();

    search_rgi_field = get_element_after_rendered(driver, elem_name=".q-field__native.q-placeholder[name='search']");
    search_rgi_field.send_keys(rgi + Keys.ENTER); #ALERT
    time.sleep(1);
    # verify client garantee
    try:
        verify_client_warning_element = driver.find_element(By.CSS_SELECTOR, "button#notification-modal-ok");
        verify_client_warning_element.click();
        time.sleep(1);
        continue;
    except:
        pass;

    see_service_orders = get_element_after_rendered(driver, ".menu--item > a[href*='ordens-de-servico']");
    see_service_orders.click();

    os_status = get_element_after_rendered(driver, "small[data-v-607cef2f]", selection_mode="all")\
                                        [OS_STATUS_POSITION_IN_TABLE];

    os_status_content = os_status.get_attribute("innerHTML").lower().strip();
    if os_status_content == "encerrado - executado":
        continue;
    elif os_status_content == "pendente":
        finish_os(driver, element_name=".q-checkbox__bg.absolute");

time.sleep(5)
driver.quit();
