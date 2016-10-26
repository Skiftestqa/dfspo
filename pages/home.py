from base import BasePage
from base import IncorrectPageException

class HomePage(BasePage):

    _landing_page_body_id = "homepage"

    def __init__(self, driver):
        super(LandingPage, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10, )
