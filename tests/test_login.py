from base_test_case import BaseTestCase
from Constants import DFS_Constants
from pages.login import LoginPage


class TestLogin(BaseTestCase):
    def setUp(self):
        super(TestLogin, self).setUp()
        self.navigate_to_page(DFS_Constants['Base_URL'] + "p/login#login")

    def test_user_can_login_with_valid_credentials(self):
        login_page_obj = LoginPage(self.driver,
                                   DFS_Constants['Username'],
                                   DFS_Constants['Password']
                                   )
        login_page_obj.login_as_valid_user()
