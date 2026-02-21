import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.config import USERNAME, PASSWORD


def test_logout(setup):

    driver = setup
    login = LoginPage(driver)
    dashboard = DashboardPage(driver)

    login.login(USERNAME, PASSWORD)
    dashboard.wait_for_dashboard_menu()

    dashboard.click_logout()

    assert login.is_login_page_displayed(), \
        "Logout failed - Login page not visible"