import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from modules.gmail_api import GmailAPI
from pages.confirm_email_page import ConfirmEmailPage
from pages.overview_page import OverviewPage


class LoginPage:

    _login_page_url = 'https://eos.com/crop-monitoring/'
    _first_name_field = (By.XPATH, "//input[@data-id='first_name']")
    _last_name_field = (By.XPATH, "//input[@data-id='last_name']")
    _email_field = (By.XPATH, "//input[@data-id='email']")
    _password_field = (By.XPATH, "//input[@data-id='password']")
    _accept_terms_checkbox = (By.XPATH, "//span[contains(@class, 'mat-checkbox-inner-container')]")
    _sign_up_button = (By.XPATH, "//button[@data-id='sign-up-btn']")
    _sign_in_form = (By.XPATH, "//button[@data-id='sign-in-button']")
    _sign_in_button = (By.XPATH, "//button[@data-id='sign-in-btn']")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self._login_page_url)
        self.wait_for_page_to_load()

    def wait_for_page_to_load(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self._sign_up_button))

    def find_element(self, strategy, locator):
        return self.driver.find_element(strategy, locator)

    @property
    def first_name_field(self):
        return self.find_element(*self._first_name_field)

    @property
    def last_name_field(self):
        return self.find_element(*self._last_name_field)

    @property
    def email_field(self):
        return self.find_element(*self._email_field)

    @property
    def password_field(self):
        return self.find_element(*self._password_field)

    @property
    def accept_terms_checkbox(self):
        return self.find_element(*self._accept_terms_checkbox)

    @property
    def sign_up_button(self):
        return self.find_element(*self._sign_up_button)

    @property
    def sign_in_form(self):
        return self.find_element(*self._sign_in_form)

    @property
    def sign_in_button(self):
        return self.find_element(*self._sign_in_button)

    def click_on_sign_up_button(self):
        self.sign_up_button.click()
        return ConfirmEmailPage(self.driver)

    def click_on_sign_in_button(self):
        self.sign_in_button.click()
        return OverviewPage(self.driver)

    @staticmethod
    def register_via_api(first_name, last_name, email, password):
        reg_url = 'https://crop-monitoring.eos.com/service/auth/account/register/'
        reg_payload = {
            "locale": "en",
            "provider": "eos_auth",
            "recaptcha_response": 1111,
            "consent_details": {
                "policy_consent": [1]
            },
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "policy_confirm": True,
            "wl": "crop_monitoring",
            "return_url": "https://crop-monitoring.eos.com/"
        }
        response = requests.post(url=reg_url, json=reg_payload)
        if response.status_code == 201:
            confirmation_code = GmailAPI().get_confirmation_code()
            conf_url = 'https://crop-monitoring.eos.com/service/auth/account/confirm/email/code/'
            conf_payload = {
                "code": confirmation_code.replace('-', ''),
                "email": email
            }
            response = requests.post(url=conf_url, json=conf_payload)
            return response.status_code == 200
        return False
