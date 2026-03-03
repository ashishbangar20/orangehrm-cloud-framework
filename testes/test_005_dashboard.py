import pytest
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.config import USERNAME, PASSWORD


@allure.feature("Dashboard Module")
class TestDashboard:

    @pytest.mark.smoke
    @allure.story("Dashboard Load After Login")
    def test_dashboard_loaded(self, setup):

        driver = setup
        login = LoginPage(driver)
        dashboard = DashboardPage(driver)

        with allure.step("Login with valid credentials"):
            login.login(USERNAME, PASSWORD)

        with allure.step("Wait for dashboard to load"):
            dashboard.wait_for_dashboard_menu()

        with allure.step("Verify dashboard is displayed"):
            assert dashboard.is_dashboard_displayed(), \
                "Dashboard did not load after login"