from selenium import webdriver;
from selenium.webdriver.chrome.service import Service;
from selenium.webdriver.common.by import By;
from selenium.webdriver.common.keys import Keys;
from utils import get_element_after_rendered, finish_os,\
                get_photos_from_urls, os_has_photos, attach_photos_from_rgi;
import pandas as pd
import numpy as np
import asyncio;

import time

data = pd.read_excel("./data_with_all_devices.xlsx").iloc[0:4, :];
RGIS = data["rgi"].unique();

service = Service(executable_path=r"./chromedriver.exe");
driver = webdriver.Chrome(service=service);

driver.get("https://aguasdejoinville.com.br/sansys/index.html");
driver.maximize_window();

time.sleep(2);

name_input = get_element_after_rendered(driver, ".q-field__native.q-placeholder[name='username']", timeout=7);
password_input = get_element_after_rendered(driver, ".q-field__native.q-placeholder[name='password']", timeout=7);
submit_login = get_element_after_rendered(driver, "[name='btn_logar']", timeout=7);

name_input.clear();
password_input.clear();

# login form
name_input.send_keys("vogel.000001");
password_input.send_keys("Caj323");
submit_login.click();
time.sleep(0.3);
submit_login.click();
menu_item = get_element_after_rendered(driver, elem_name="button[name='menuItem']");
OS_STATUS_POSITION_IN_TABLE = 3;

async def main():

    for i, rgi in enumerate(RGIS):
        subdata = data[data["rgi"]==rgi];
        meter_code = f"Número do medidor: {subdata['meter_serial_number'].unique()[0]}";
        executed_at = f"Data da execução do serviço: {subdata['created_at'].unique()[0]}";
        last_reading = f"Leitura: {subdata['current_reading'].unique()[0]}";
        module_number = f"Número do módulo: {subdata['device_serial_number'].unique()[0]}";
        photo_urls = subdata["photo_link"].unique();
        data_to_deletion = [meter_code, executed_at, last_reading, module_number];
        menu_item.click();
        # from the first iteration, the link will be already open. No need to expand it again
        if i == 0:
            attendence_button = get_element_after_rendered(driver, elem_name="div[name='M00003']",);
            attendence_button.click();

        time.sleep(0.7);
        start_attendence_link = get_element_after_rendered(driver, elem_name="a[href='#/interno/atendimento']");
        start_attendence_link.click();

        search_rgi_field = get_element_after_rendered(driver, elem_name=".q-field__native.q-placeholder[name='search']");
        search_rgi_field.clear();
        time.sleep(1);
        search_rgi_field.send_keys(rgi + Keys.ENTER); #ALERT
        # verify client garantee
        try:
            time.sleep(1);
            verify_client_warning_element = driver.find_element(By.CSS_SELECTOR, "button#notification-modal-ok");
            verify_client_warning_element.click();
        except:
            pass;

        see_service_orders = get_element_after_rendered(driver, ".menu--item > a[href*='ordens-de-servico']");
        see_service_orders.click();

        os_status = get_element_after_rendered(driver, "small[data-v-607cef2f]", selection_mode="all")\
                                            [OS_STATUS_POSITION_IN_TABLE];

        os_status_content = os_status.get_attribute("innerHTML").lower().strip();
        if os_status_content == "pendente":
            photos_status, photo_element = os_has_photos(driver);
            if photos_status == False:
                await get_photos_from_urls(rgi, photo_urls);
                attach_photos_from_rgi(driver, rgi, photo_element);
            finish_os(driver, element_name=".q-checkbox__bg.absolute", os_data=data_to_deletion);
        elif os_status_content == "encerrado - executado":
            photos_status, photo_element = os_has_photos(driver);
            if photos_status == False:
                await get_photos_from_urls(rgi, photo_urls);
                attach_photos_from_rgi(driver, rgi, photo_element);
            continue;

    time.sleep(5);
    driver.quit();

if __name__ == '__main__':
    asyncio.run(main());
