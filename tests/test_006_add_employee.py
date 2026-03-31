import pytest
import allure
import time
import random

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.pim_page import PimPage
from pages.add_employee_page import AddEmployeePage
from utils.json_reader import JsonReader
from config.config import USERNAME, PASSWORD


@allure.feature("PIM Module")
class TestAddEmployeeE2E:

    @pytest.mark.smoke
    @allure.story("Add Employee End to End Flow")
    def test_add_employee_e2e(self, setup):

        driver = setup

        login = LoginPage(driver)
        dashboard = DashboardPage(driver)
        pim = PimPage(driver)
        add_emp = AddEmployeePage(driver)

        reader = JsonReader("testData/test_data.json")
        data = reader.get_test_data("add_employee")

        if isinstance(data, list):
            data = data[0]

        unique_id = str(random.randint(1000, 9999))
        unique_username = data["username"] + str(int(time.time()))

        with allure.step("Login with valid credentials"):
            login.login(USERNAME, PASSWORD)

        with allure.step("Wait for dashboard to load"):
            dashboard.wait_for_dashboard_menu()

        with allure.step("Navigate to PIM module"):
            dashboard.click_pim()

        with allure.step("Click Add Employee"):
            pim.click_add_employee()

        with allure.step("Wait for Add Employee page"):
            add_emp.wait_for_add_employee_page()

        with allure.step("Enter employee details"):
            add_emp.enter_first_name(data["first_name"])
            add_emp.enter_middle_name(data["middle_name"])
            add_emp.enter_last_name(data["last_name"])
            add_emp.enter_employee_id(unique_id)

        with allure.step("Enable login credentials"):
            add_emp.enable_login_details()

        with allure.step("Enter login credentials"):
            add_emp.enter_username(unique_username)
            add_emp.enter_password(data["password"])
            add_emp.enter_confirm_password(data["password"])

        with allure.step("Save employee"):
            add_emp.click_save()

        with allure.step("Verify employee created successfully"):
            add_emp.wait_for_personal_details_page()
            assert add_emp.is_personal_details_page_loaded()

            print(f"\nEmployee Created: {unique_username} | ID: {unique_id}")