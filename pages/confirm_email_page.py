from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.overview_page import OverviewPage


class ConfirmEmailPage:

    _submit_code_button = (By.XPATH, "//button[@data-id='submit-code-btn']")
    _confirm_code_field = (By.XPATH, "//input[@data-id='confirm-code-input']")

    def __init__(self, driver):
        self.driver = driver
        self.wait_for_page_to_load()

    def wait_for_page_to_load(self):
        return WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self._submit_code_button))

    def find_element(self, strategy, locator):
        return self.driver.find_element(strategy, locator)

    @property
    def submit_code_button(self):
        return self.find_element(*self._submit_code_button)

    @property
    def confirm_code_field(self):
        return self.find_element(*self._confirm_code_field)

    def enter_confirm_code(self, code):
        self.confirm_code_field.send_keys(code)
        return OverviewPage(self.driver)
