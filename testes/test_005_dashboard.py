import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.config import USERNAME, PASSWORD


def test_dashboard_loaded(setup):

    driver = setup
    login = LoginPage(driver)
    dashboard = DashboardPage(driver)

    login.login(USERNAME, PASSWORD)
    dashboard.wait_for_dashboard_menu()

    assert dashboard.is_dashboard_displayed(), \
        "Dashboard did not load after login"