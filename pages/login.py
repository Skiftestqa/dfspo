import time

from base import BasePage
from base import IncorrectPageException


class LoginPage(BasePage):
    _email_id_locator = "email"
    _password_id_locator = "password"
    _login_button_name_locator = "login"
    _failure_login_id_locator = "ccf1.email.e"
    _warning_popup_locator = "div.warning"
    _too_many_attempts_failure_message_locator = "div.warning:contains('Too many failed attempts.')"
    _invalid_email_and_password_locator = "ccf1.email.e"
    _please_enter_password_prompt_locator = "ccf1.password.e"

    def __init__(self, driver):
        super(LoginPage, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10, "id", self._email_id_locator)
        except:
            raise IncorrectPageException

    def login_as_valid_user(self, username, password):
        self.fill_out_field("id", self._email_id_locator, username)
        self.fill_out_field("id", self._password_id_locator, password)
        self.click(10, "name", self._login_button_name_locator)
        from lobby import LobbyPage
        return LobbyPage(self.driver)

    def login_as_invalid_user(self):
        self.fill_out_field("id", self._email_id_locator, "bad@email.com")
        self.fill_out_field("id", self._password_id_locator, "badpassword")
        self.click(10, "name", self._login_button_name_locator)

    def login_invalid_email_and_password_prompt_present(self):
        self.wait_for_element_visibility(10, "id", self._invalid_email_and_password_locator)
        return self.find_element("id", self._invalid_email_and_password_locator).is_displayed()

    def login_two_attempts_in_two_seconds(self):
        for i in range(2):
            self.fill_out_field("id", self._email_id_locator, "bad@email.com")
            self.fill_out_field("id", self._password_id_locator, "badpassword123")
            self.click(10, "name", self._login_button_name_locator)
            time.sleep(1)

    def login_try_again_in_one_minute_message_present(self):
        alert = self.wait_for_element_visibility(10, "css", self._warning_popup_locator)
        alert_text = alert.text
        if "Please wait 1 minute before trying again." in alert_text:
            return True
        else:
            return False

    def login_with_invalid_email_and_no_password(self):
        self.fill_out_field("id", self._email_id_locator, "bad@email.com")
        self.click(10, "name", self._login_button_name_locator)

    def login_enter_password_prompt_present(self):
        self.wait_for_element_visibility(10, "id", self._please_enter_password_prompt_locator)
        return self.find_element("id", self._please_enter_password_prompt_locator).is_displayed()
