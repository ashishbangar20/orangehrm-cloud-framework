import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


@pytest.mark.parametrize(
    "username,password,expected",
    [
        ("Admin", "admin123", True),
        ("Admin", "wrongpass", False),
        ("WrongUser", "admin123", False),
        ("WrongUser", "wrongpass", False),
    ]
)
def test_login_param(setup, username, password, expected):

    driver = setup
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)

    login_page.login(username, password)

    if expected:
        dashboard_page.wait_for_dashboard_menu()
        assert dashboard_page.is_dashboard_displayed()
        dashboard_page.click_logout()
    else:
        assert login_page.is_login_error_displayed()