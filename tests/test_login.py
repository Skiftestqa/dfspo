import pytest
from constants import dfs_constants
from pages.home import HomePage


class TestLogin():

    @pytest.fixture
    def home_page_obj(self, driver):
        return HomePage(driver)

    def test_user_can_login_with_valid_credentials(self, home_page_obj):
        login_page_obj = home_page_obj.click_login_button()
        login_page_obj.login_as_valid_user(dfs_constants['Username'],
                                           dfs_constants['Password'])
