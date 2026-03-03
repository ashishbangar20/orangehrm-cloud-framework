import pytest
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


@allure.feature("Authentication Module")
class TestLoginParameterized:

    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "username,password,expected",
        [
            ("Admin", "admin123", True),
            ("Admin", "wrongpass", False),
            ("WrongUser", "admin123", False),
            ("WrongUser", "wrongpass", False),
        ]
    )
    @allure.story("Parameterized Login Validation")
    def test_login_param(self, setup, username, password, expected):

        driver = setup
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)

        with allure.step(f"Login with username: {username} and password: {password}"):
            login_page.login(username, password)

        if expected:
            with allure.step("Verify dashboard is displayed"):
                dashboard_page.wait_for_dashboard_menu()
                assert dashboard_page.is_dashboard_displayed(), \
                    "Dashboard not displayed after valid login"

            with allure.step("Logout after successful login"):
                dashboard_page.click_logout()
        else:
            with allure.step("Verify login error message is displayed"):
                assert login_page.is_login_error_displayed(), \
                    "Error message not displayed for invalid login"