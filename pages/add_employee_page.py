from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class AddEmployeePage(BasePage):

    # =========================
    # LOCATORS
    # =========================
    ADD_EMPLOYEE_HEADER = (By.XPATH, "//h6[text()='Add Employee']")
    PERSONAL_DETAILS_HEADER = (By.XPATH, "//h6[text()='Personal Details']")

    FIRST_NAME = (By.NAME, "firstName")
    MIDDLE_NAME = (By.NAME, "middleName")
    LAST_NAME = (By.NAME, "lastName")

    EMPLOYEE_ID = (By.XPATH, "//label[text()='Employee Id']/../following-sibling::div//input")

    CREATE_LOGIN_TOGGLE = (By.XPATH, "//span[contains(@class,'oxd-switch-input')]")

    USERNAME = (By.XPATH, "//label[text()='Username']/../following-sibling::div//input")
    PASSWORD = (By.XPATH, "//label[text()='Password']/../following-sibling::div//input")
    CONFIRM_PASSWORD = (By.XPATH, "//label[text()='Confirm Password']/../following-sibling::div//input")

    SAVE_BUTTON = (By.XPATH, "//button[@type='submit']")

    # =========================
    # PAGE VALIDATION
    # =========================

    def wait_for_add_employee_page(self):
        return self.find_visible_element(self.ADD_EMPLOYEE_HEADER)

    def is_add_employee_page_displayed(self):
        return self.is_element_displayed(self.ADD_EMPLOYEE_HEADER)

    def wait_for_personal_details_page(self):
        return self.find_visible_element(self.PERSONAL_DETAILS_HEADER)

    def is_personal_details_page_loaded(self):
        return self.is_element_displayed(self.PERSONAL_DETAILS_HEADER)

    # =========================
    # FORM ACTIONS
    # =========================

    def enter_first_name(self, value):
        self.type(self.FIRST_NAME, value)

    def enter_middle_name(self, value):
        self.type(self.MIDDLE_NAME, value)

    def enter_last_name(self, value):
        self.type(self.LAST_NAME, value)

    def enter_employee_id(self, value):
        self.type(self.EMPLOYEE_ID, value)

    def enable_login_details(self):
        self.find_visible_element(self.CREATE_LOGIN_TOGGLE)
        self.click(self.CREATE_LOGIN_TOGGLE)

    def enter_username(self, value):
        self.type(self.USERNAME, value)

    def enter_password(self, value):
        self.type(self.PASSWORD, value)

    def enter_confirm_password(self, value):
        self.type(self.CONFIRM_PASSWORD, value)

    def click_save(self):
        self.find_visible_element(self.SAVE_BUTTON)  # wait
        self.click(self.SAVE_BUTTON)