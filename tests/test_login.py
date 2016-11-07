from base_test_case import BaseTestCase
from Constants import DFS_Constants
from pages.home import HomePage


class TestLogin(BaseTestCase):
    def setUp(self):
        super(TestLogin, self).setUp()
        self.navigate_to_page(DFS_Constants['Base_URL'])

    def test_user_can_login_with_valid_credentials(self):
        home_page_obj = HomePage(self.driver)
        login_page_obj = home_page_obj.click_login_button()
        login_page_obj.login_as_valid_user(DFS_Constants['Username'],
                                           DFS_Constants['Password'])
