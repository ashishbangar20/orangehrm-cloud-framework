import pytest
from pages.login_page import LoginPage
from config.config import USERNAME, PASSWORD


class TestLogin:

    @pytest.mark.smoke
    def test_login_valid(self, setup):

        driver = setup
        login_page = LoginPage(driver)

        login_page.login(USERNAME, PASSWORD)

        assert "dashboard" in driver.current_url.lower()