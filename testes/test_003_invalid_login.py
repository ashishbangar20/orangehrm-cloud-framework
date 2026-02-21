import pytest
from pages.login_page import LoginPage


def test_invalid_login(setup):

    driver = setup
    login = LoginPage(driver)

    login.enter_username("Admin")
    login.enter_password("wrongpass")
    login.click_login()

    assert login.is_login_error_displayed(), \
        "Error message not displayed for invalid login"