import pytest

from dfspo.constants import dfs_constants
from dfspo.pages.home import HomePage


class TestLogin():
    @pytest.fixture()
    def home_page_obj(self, driver):
        return HomePage(driver)

    @pytest.mark.shallow
    def test_user_can_login_with_valid_credentials(self, home_page_obj):
        login_page_obj = home_page_obj.click_login_button()
        login_page_obj.login_as_valid_user(dfs_constants['Username'],
                                           dfs_constants['Password'])

    @pytest.mark.deep
    def test_user_cannot_login_with_invalid_credentials(self, home_page_obj):
        login_page_obj = home_page_obj.click_login_button()
        login_page_obj.login_as_invalid_user()
        assert login_page_obj.login_invalid_email_and_password_prompt_present() == True

    @pytest.mark.deep
    def test_alert_message_present(self, home_page_obj):
        login_page_obj = home_page_obj.click_login_button()
        login_page_obj.login_two_attempts_in_two_seconds()
        assert login_page_obj.login_try_again_in_one_minute_message_present() == True

    @pytest.mark.deep
    def test_please_enter_password_prompt_present(self, home_page_obj):
        login_page_obj = home_page_obj.click_login_button()
        login_page_obj.login_with_invalid_email_and_no_password()
        assert login_page_obj.login_enter_password_prompt_present() == True
