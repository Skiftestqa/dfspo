from base import BasePage
from base import IncorrectPageException
from join import JoinPage

class HomePage(BasePage):

    _body_id = "#homepage"
    _join_button = "div.join-menu-block > a"
    _login_button = ".global-header-container .login-menu-block > a"

    def __init__(self, driver):
        super(HomePage, self).__init__(driver)

    def _verify_page(self):
        try:
            self.wait_for_element_visibility(10, "id", _body_id)
        except:
            raise IncorrectPageException

    def join(self):
    	self.click(10, "css", _join_button)
    	return JoinPage(self.driver)

    def login(self):
    	self.click(10, "")	


