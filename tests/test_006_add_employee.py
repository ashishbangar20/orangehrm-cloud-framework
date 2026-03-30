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

        # Page Objects
        login = LoginPage(driver)
        dashboard = DashboardPage(driver)
        pim = PimPage(driver)
        add_emp = AddEmployeePage(driver)

        # -------------------------------
        # Test Data
        # -------------------------------
        reader = JsonReader("testData/test_data.json")
        data = reader.get_test_data("add_employee")

        if isinstance(data, list):
            data = data[0]

        # 🔥 Dynamic data (avoid duplicates)
        unique_id = str(random.randint(1000, 9999))
        unique_username = data["username"] + str(int(time.time()))

        # -------------------------------
        # STEP 1: Login
        # -------------------------------
        with allure.step("Login with valid credentials"):
            login.login(USERNAME, PASSWORD)

        # -------------------------------
        # STEP 2: Wait Dashboard
        # -------------------------------
        with allure.step("Wait for dashboard to load"):
            dashboard.wait_for_dashboard_menu()

        # -------------------------------
        # STEP 3: Navigate to PIM
        # -------------------------------
        with allure.step("Navigate to PIM module"):
            dashboard.click_pim()

        # -------------------------------
        # STEP 4: Click Add Employee
        # -------------------------------
        with allure.step("Click Add Employee"):
            pim.click_add_employee()

        # -------------------------------
        # STEP 5: Wait Add Employee Page
        # -------------------------------
        with allure.step("Wait for Add Employee page"):
            add_emp.wait_for_add_employee_page()

        # -------------------------------
        # STEP 6: Enter Basic Details
        # -------------------------------
        with allure.step("Enter employee details"):
            add_emp.enter_first_name(data["first_name"])
            add_emp.enter_middle_name(data["middle_name"])
            add_emp.enter_last_name(data["last_name"])
            add_emp.enter_employee_id(unique_id)

        # -------------------------------
        # STEP 7: Enable Login Details
        # -------------------------------
        with allure.step("Enable login credentials"):
            add_emp.enable_login_details()

        # -------------------------------
        # STEP 8: Enter Login Credentials
        # -------------------------------
        with allure.step("Enter login credentials"):
            add_emp.enter_username(unique_username)
            add_emp.enter_password(data["password"])
            add_emp.enter_confirm_password(data["password"])

        # -------------------------------
        # STEP 9: Save Employee
        # -------------------------------
        with allure.step("Save employee"):
            add_emp.click_save()

        # -------------------------------
        # STEP 10: Verify (FIXED 🔥)
        # -------------------------------
        with allure.step("Verify employee created successfully"):

            # Wait for success page
            add_emp.wait_for_personal_details_page()

            # Validate using UI element (NOT URL ❌)
            assert add_emp.is_personal_details_page_loaded(), \
                "Employee creation failed ❌"

            print(f"\n✅ Employee Created: {unique_username} | ID: {unique_id}")