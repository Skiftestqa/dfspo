from base import BasePage
from base import IncorrectPageException


class LoginPage(BasePage):
    _email_id = "email"
    _password_id = "password"
    _login_button_name = "login"

    def __init__(self, driver, username, password):
        super(LoginPage, self).__init__(driver)
        self.username = username
        self.password = password

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10, "id", _email_id)
        except:
            raise IncorrectPageException

    def login_as_valid_user(self):
        self.fill_out_field("id", _email_id, self.username)
        self.fill_out_field("id", _password_id, self.password)
        self.click(10, "name", _login_button_name)
        from lobby import LobbyPage
        return LobbyPage(self.driver)

    def login_as_invalid_user(self):
        pass
