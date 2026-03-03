import pytest
import allure
from pages.login_page import LoginPage


@allure.feature("Authentication Module")
class TestInvalidLogin:

    @pytest.mark.smoke
    @allure.story("Invalid Login")
    def test_invalid_login(self, setup):

        driver = setup
        login = LoginPage(driver)

        with allure.step("Enter valid username"):
            login.enter_username("Admin")

        with allure.step("Enter invalid password"):
            login.enter_password("wrongpass")

        with allure.step("Click login button"):
            login.click_login()

        with allure.step("Verify error message is displayed"):
            assert login.is_login_error_displayed(), \
                "Error message not displayed for invalid login"