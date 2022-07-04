from faker import Faker

from modules.utils import generate_random_string


class User:

    def __init__(self):
        self._first_name = Faker().first_name()
        self._last_name = Faker().last_name()
        self._email = f"testtaskeos+{generate_random_string(5)}@gmail.com"
        self._password = Faker().password()

    def get_first_name(self):
        return self._first_name

    def get_last_name(self):
        return self._last_name

    def get_email(self):
        return self._email

    def get_password(self):
        return self._password
