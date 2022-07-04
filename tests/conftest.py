import os

import pytest

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeOptions

from modules.gmail_api import GmailAPI


@pytest.fixture(scope='function', autouse=True)
def driver():
    options = ChromeOptions()
    options.headless = bool(os.getenv('HEADLESS', 'false'))
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                              options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope='function', autouse=True)
def setup_function():
    GmailAPI().remove_all_emails()
