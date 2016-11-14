from base import BasePage
from base import IncorrectPageException

class LoginPage(BasePage):
    _email_id_locator = "email"
    _password_id_locator = "password"
    _login_button_name_locator = "login"

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
        pass
