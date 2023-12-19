from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.common.by import By;
from selenium.webdriver.support import expected_conditions as EC;


def get_element_after_rendered(driver, elem_name:str, selector:By = By.CSS_SELECTOR, timeout:int = 5):
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
    WebDriverWait(driver, timeout) \
        .until(EC.presence_of_element_located((selector, elem_name)));
    element_in_html = driver.find_element(selector, elem_name);
    return element_in_html;