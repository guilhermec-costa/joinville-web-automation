from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.common.by import By;
from selenium.webdriver.support import expected_conditions as EC;
from selenium import webdriver;
from selenium.webdriver.remote.webelement import WebElement;
from selenium.webdriver.common.keys import Keys;
import pyautogui;
import aiohttp;
import asyncio;
import shutil;
import time;
import os;

def get_element_after_rendered(driver:webdriver.Chrome, elem_name:str, selector:By = By.CSS_SELECTOR,
                               timeout:int = 5, selection_mode:str = "single") -> WebElement:
    """
        Waits for an element to be rendered on the screen,
        and only then selects it.

        Args:
            elem_name (str) : name of the element to be searched.
            selector (By.{SELECTOR}) : type of HTML identifier to perform the search.
            timeout (int) : time to wait until the element be rendered.
        Returns:
            element_in_html (WebElement) : a HTML element representation.
    """

    find_by_switcher = {
    "single": driver.find_element,
    "all": driver.find_elements
    }


    WebDriverWait(driver, timeout) \
        .until(EC.presence_of_element_located((selector, elem_name)));
    element_in_html = find_by_switcher[selection_mode](selector, elem_name);
    return element_in_html;


def finish_os(driver: webdriver.Chrome, element_name: str, **kwargs):
    data = kwargs["os_data"];
    choosed_os = get_element_after_rendered(driver, element_name, selection_mode="all")[0];
    choosed_os.click();

    deletion_confirmation_btn = get_element_after_rendered(driver, "button[name='SHUT']");
    deletion_confirmation_btn.click();

    second_confirmation = driver.find_element(By.XPATH, '//div[contains(text(), "Encerrar Ordem de Serviço")]');
    second_confirmation.click();

    text_area = get_element_after_rendered(driver, "textarea[name='parecer']");
    for line in data:
        text_area.send_keys(f"{line}\n");
    
    next_step_btn1 = get_element_after_rendered(driver, ".q-btn.q-btn-item.non-selectable.no-outline.q-px-md.q-btn--standard.q-btn--rectangle.bg-grey-4.text-dark.q-btn--actionable.q-focusable.q-hoverable.q-btn--wrap")
    next_step_btn1.click();

    equip_id_input = get_element_after_rendered(driver, "input#idEquipe");
    equip_id_input.send_keys("vogel01" + Keys.ENTER);
    next_step_btn2 = driver.find_element(By.CSS_SELECTOR, "button#next");
    time.sleep(1);
    next_step_btn2.click();
    add_case_btm = driver.find_element(By.CSS_SELECTOR, ".q-btn.q-btn-item.non-selectable.no-outline.btnSave.q-btn--standard.q-btn--rectangle.bg-info.text-white.q-btn--actionable.q-focusable.q-hoverable.q-btn--wrap")
    time.sleep(1);
    add_case_btm.click();
    finish_deletion = driver.find_element(By.CSS_SELECTOR, "button#finish");
    time.sleep(1);
    finish_deletion.click();


async def fetch(session:aiohttp.ClientSession, url, url_index, directory):
    async with session.get(url) as req:
        if req.status == 200:
            with open(fr"{directory}/image{url_index}.jpg", "wb") as handler:
                handler.write(await req.read());


async def fetch_all(session:aiohttp.ClientSession, urls, directory):
    tasks = [];
    for i, url in enumerate(urls):
        new_task = asyncio.create_task(fetch(session, url, i, directory));
        tasks.append(new_task);
    await asyncio.gather(*tasks);

async def get_photos_from_urls(rgi, photo_urls):
    dir_to_create = fr"./{rgi}"
    os.mkdir(dir_to_create);
    async with aiohttp.ClientSession() as session:
        await fetch_all(session, photo_urls, dir_to_create);
    # os.rmdir(dir_to_create);

def os_has_photos(driver:webdriver.Chrome):
    add_photo_element = driver.find_element(By.XPATH, "//i[contains(@class, 'material-icons')][@data-v-607cef2f]");
    element_classes:str = add_photo_element.get_attribute("class");
    return (False, add_photo_element) if "grey" in element_classes else (True, None);

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size();
def attach_photos_from_rgi(driver:webdriver.Chrome, rgi, photo_element: WebElement):
    qty_of_photos = len([photo for photo in os.scandir(f"./{rgi}")])
    time.sleep(1);
    photo_element.click();
    time.sleep(1);
    attach_multiple_photos_elem = driver.find_element(By.CSS_SELECTOR, "a[role='button']");
    time.sleep(1);
    attach_multiple_photos_elem.click();
    time.sleep(1.5);
    pyautogui.moveTo(SCREEN_WIDTH/2, SCREEN_HEIGHT/2);
    pyautogui.click(); # activates the current folder window that opens after the input click
    pyautogui.hotkey("altleft", "home");
    time.sleep(0.8);
    photos_to_look_at = os.path.abspath(os.getcwd()) + f"/{rgi}/ "; # the empty space is essencial, to not autocomplete
    pyautogui.hotkey("ctrlleft", "l");
    time.sleep(1);
    pyautogui.write(photos_to_look_at, interval=0.06);
    pyautogui.press("enter");
    time.sleep(1);
    pyautogui.moveTo(SCREEN_WIDTH/2, SCREEN_HEIGHT/2);
    pyautogui.click(); # activates the current folder window that opens after the input click
    time.sleep(2);
    pyautogui.hotkey("ctrlleft", "a");
    time.sleep(1);
    pyautogui.press("enter");
    time.sleep(1.5);
    photo_interactions_btns = driver.find_elements(By.CSS_SELECTOR, ".q-btn.q-btn-item.non-selectable.no-outline.q-btn--flat.q-btn--rectangle.q-btn--actionable.q-focusable.q-hoverable.q-btn--wrap.q-btn--dense");
    confirm_photos_attach_btn = photo_interactions_btns[-1];
    time.sleep(1);
    confirm_photos_attach_btn.click();
    time.sleep(qty_of_photos * 1.7);
    close_window_btn = driver.find_element(By.XPATH, "//i[contains(text(), 'cancel') and @role='img' and @aria-hidden='true']");
    time.sleep(1.3)
    print(close_window_btn.get_attribute("class"));
    close_window_btn.click();
    time.sleep(5);
    shutil.rmtree(f"./{rgi}");
