from base import BasePage
from base import IncorrectPageException


class HomePage(BasePage):

    _body_id_locator = "homepage"
    _join_button_locator = "div.join-menu-block > a"
    _login_button_locator = ".global-header-container .login-menu-block > a"

    def __init__(self, driver):
        super(HomePage, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10, "id", self._body_id_locator)
        except:
            raise IncorrectPageException

    def click_join_button(self):
        self.click(10, "css", self._join_button_locator)
        from join import JoinPage
        return JoinPage(self.driver)

    def click_login_button(self):
        self.click(10, "css", self._login_button_locator)
        from login import LoginPage
        return LoginPage(self.driver)
