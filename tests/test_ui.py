import time
from modules.gmail_api import GmailAPI
from modules.user import User
from pages.login_page import LoginPage


def test_registration(driver):
    login_page = LoginPage(driver)
    login_page.open()
    user = User()

    login_page.first_name_field.send_keys(user.get_first_name())
    login_page.last_name_field.send_keys(user.get_last_name())
    login_page.email_field.send_keys(user.get_email())
    login_page.password_field.send_keys(user.get_password())
    login_page.accept_terms_checkbox.click()
    time.sleep(3)
    confirm_email_page = login_page.click_on_sign_up_button()

    confirmation_code = GmailAPI().get_confirmation_code()
    overview_page = confirm_email_page.enter_confirm_code(confirmation_code)
    assert overview_page.wait_for_page_to_load()


def test_login(driver):
    login_page = LoginPage(driver)
    user = User()
    assert login_page.register_via_api(user.get_first_name(),
                                       user.get_last_name(),
                                       user.get_email(),
                                       user.get_password())

    login_page.open()
    login_page.sign_in_form.click()
    login_page.email_field.send_keys(user.get_email())
    login_page.password_field.send_keys(user.get_password())

    overview_page = login_page.click_on_sign_in_button()
    assert overview_page.wait_for_page_to_load()
