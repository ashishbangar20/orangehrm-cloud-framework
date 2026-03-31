from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class PimPage(BasePage):

    ADD_EMPLOYEE_BTN = (By.XPATH, "//button[contains(., 'Add')]")
    PERSONAL_DETAILS_HEADER = (By.XPATH, "//h6[text()='Personal Details']")

    def click_add_employee(self):
        self.find_visible_element((By.XPATH, "//h6[text()='PIM']"), timeout=20)
        self.find_visible_element(self.ADD_EMPLOYEE_BTN, timeout=20)
        self.click(self.ADD_EMPLOYEE_BTN)

    def is_personal_details_page_loaded(self):
        return self.is_element_displayed(self.PERSONAL_DETAILS_HEADER)