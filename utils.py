from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.common.by import By;
from selenium.webdriver.support import expected_conditions as EC;
from selenium import webdriver;

def get_element_after_rendered(driver:webdriver.Chrome, elem_name:str, selector:By = By.CSS_SELECTOR,
                               timeout:int = 5, selection_mode:str = "single"):
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


def finish_os(driver: webdriver.Chrome, element_name: str):
    choosed_os = get_element_after_rendered(driver, element_name, selection_mode="all")[0];
    choosed_os.click();

    deletion_confirmation_btn = get_element_after_rendered(driver, "button[name='SHUT']");
    deletion_confirmation_btn.click();

    second_confirmation = driver.find_element(By.XPATH, '//div[contains(text(), "Encerrar Ordem de Serviço")]');
    second_confirmation.click();
    return;
