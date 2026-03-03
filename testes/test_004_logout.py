import pytest
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.config import USERNAME, PASSWORD


@allure.feature("Authentication Module")
class TestLogout:

    @pytest.mark.smoke
    @allure.story("User Logout")
    def test_logout(self, setup):

        driver = setup
        login = LoginPage(driver)
        dashboard = DashboardPage(driver)

        with allure.step("Login with valid credentials"):
            login.login(USERNAME, PASSWORD)

        with allure.step("Wait for dashboard to load"):
            dashboard.wait_for_dashboard_menu()

        with allure.step("Click logout button"):
            dashboard.click_logout()

        with allure.step("Verify login page is displayed after logout"):
            assert login.is_login_page_displayed(), \
                "Logout failed - Login page not visible"