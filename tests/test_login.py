import pytest
from dfspo.constants import dfs_constants
from dfspo.pages.home import HomePage


class TestLogin():

    @pytest.fixture
    def home_page_obj(self, driver):
        return HomePage(driver)

    def test_user_can_login_with_valid_credentials(self, home_page_obj):
        login_page_obj = home_page_obj.click_login_button()
        login_page_obj.login_as_valid_user(dfs_constants['Username'],
                                           dfs_constants['Password'])

    def test_user_cannot_login_with_invalid_credentials(self, home_page_obj):
        login_page_obj = home_page_obj.click_login_button()
        login_page_obj.login_as_invalid_user()
        assert login_page_obj.login_failure_message_is_present() == True
