from base_test_case import BaseTestCase
from constants import dfs_constants
from pages.home import HomePage


class TestLogin(BaseTestCase):
    def setUp(self):
        super(TestLogin, self).setUp()
        self.navigate_to_page(dfs_constants['Base_URL'])

    def test_user_can_login_with_valid_credentials(self):
        home_page_obj = HomePage(self.driver)
        login_page_obj = home_page_obj.click_login_button()
        login_page_obj.login_as_valid_user(dfs_constants['Username'],
                                           dfs_constants['Password'])
