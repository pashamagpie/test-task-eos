from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class OverviewPage:

    _trial_modal_window = (By.ID, 'mat-dialog-0')

    def __init__(self, driver):
        self.driver = driver
        self.wait_for_page_to_load()

    def find_element(self, strategy, locator):
        return self.driver.find_element(strategy, locator)

    def wait_for_page_to_load(self):
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self._trial_modal_window))
