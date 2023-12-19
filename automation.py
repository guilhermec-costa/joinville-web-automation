from selenium import webdriver;
from selenium.webdriver.chrome.service import Service;
from selenium.webdriver.common.by import By;
from selenium.webdriver.common.keys import Keys;
from utils import get_element_after_rendered;

import time



service = Service(executable_path=r"chromedriver.exe");
driver = webdriver.Chrome(service=service);

driver.get("https://aguasdejoinville.com.br/sansys/index.html");
driver.maximize_window();

time.sleep(2);

name_input = driver.find_element(By.CSS_SELECTOR, ".q-field__native.q-placeholder[name='username']");
password_input = driver.find_element(By.CSS_SELECTOR, ".q-field__native.q-placeholder[name='password']");
submit_login = driver.find_element(By.CSS_SELECTOR, "[name='btn_logar']");

name_input.clear();
password_input.clear();

name_input.send_keys("vogel.000001");
password_input.send_keys("Caj323");
submit_login.click();
time.sleep(0.3);
submit_login.click();

menu_item = get_element_after_rendered(driver, elem_name="button[name='menuItem']",)
menu_item.click();

attendence_button = get_element_after_rendered(driver, elem_name="div[name='M00003']",)
attendence_button.click();

start_attendence_link = get_element_after_rendered(driver, elem_name="Iniciar Atendimento",
                                                   selector=By.PARTIAL_LINK_TEXT)
start_attendence_link.click();

search_rgi_field = get_element_after_rendered(driver, elem_name=".q-field__native.q-placeholder[name='search']");
time.sleep(5);
search_rgi_field.send_keys("00213910-3" + Keys.ENTER);

see_service_orders = get_element_after_rendered(driver, ".menu--item > a[href*='ordens-de-servico']");
see_service_orders.click();

time.sleep(3);
driver.quit();
