from base import BasePage
from base import IncorrectPageException


class JoinPage(BasePage):
    _signup_form_locator = "signupForm"

    def __init__(self, driver):
        super(JoinPage, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10, "id", self._signup_form_locator)
        except:
            raise IncorrectPageException
