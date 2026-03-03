import pytest
import allure
from pages.login_page import LoginPage
from config.config import USERNAME, PASSWORD


@allure.feature("Authentication Module")
class TestLogin:

    @pytest.mark.smoke
    @allure.story("Valid Login")
    @allure.title("Verify user can login with valid credentials")
    def test_login_valid(self, setup):

        driver = setup
        login_page = LoginPage(driver)

        with allure.step("Enter valid username and password"):
            login_page.login(USERNAME, PASSWORD)

        with allure.step("Verify user is redirected to dashboard"):
            assert "dashboard" in driver.current_url.lower(), \
                "User was not redirected to Dashboard"