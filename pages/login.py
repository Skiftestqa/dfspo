from base import BasePage
from base import IncorrectPageException


class LoginPage(BasePage):
    _email_id_locator = "email"
    _password_id_locator = "password"
    _login_button_name_locator = "login"

    def __init__(self, driver, username, password):
        super(LoginPage, self).__init__(driver)
        self.username = username
        self.password = password

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10, "id", self._email_id_locator)
        except:
            raise IncorrectPageException

    def login_as_valid_user(self):
        self.fill_out_field("id", self._email_id_locator, self.username)
        self.fill_out_field("id", self._password_id_locator, self.password)
        self.click(10, "name", self._login_button_name_locator)
        from lobby import LobbyPage
        return LobbyPage(self.driver)

    def login_as_invalid_user(self):
        pass
