from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class PimPage(BasePage):

    ADD_EMPLOYEE_BTN = (By.XPATH, "//a[text()='Add Employee']")
    PERSONAL_DETAILS_HEADER = (By.XPATH, "//h6[text()='Personal Details']")

    def click_add_employee(self):
        self.find_visible_element(self.ADD_EMPLOYEE_BTN)  # wait
        self.click(self.ADD_EMPLOYEE_BTN)

    def is_personal_details_page_loaded(self):
        return self.is_element_displayed(self.PERSONAL_DETAILS_HEADER)