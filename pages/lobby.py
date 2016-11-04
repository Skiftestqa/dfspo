from base import BasePage
from base import IncorrectPageException


class LobbyPage(BasePage):

    _create_contest_button_locator = "div[class*='lobby-header__create'] > a"

    def __init__(self, driver):
        super(LobbyPage, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10, "css", self._create_contest_button_locator)
        except:
            raise IncorrectPageException
