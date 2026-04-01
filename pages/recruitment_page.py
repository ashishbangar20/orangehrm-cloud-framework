from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class RecruitmentPage(BasePage):

    # 🔹 Locators
    RECRUITMENT_MENU = (By.XPATH, "//span[text()='Recruitment']")
    ADD_BUTTON = (By.XPATH, "//button[normalize-space()='Add']")

    FIRST_NAME = (By.NAME, "firstName")
    LAST_NAME = (By.NAME, "lastName")
    EMAIL = (By.XPATH, "//label[text()='Email']/../following-sibling::div//input")

    SAVE_BUTTON = (By.XPATH, "//button[@type='submit']")
    SUCCESS_TOAST = (By.XPATH, "//div[contains(@class,'toast')]")

    # 🔹 Navigation
    def go_to_recruitment(self):
        self.click(self.RECRUITMENT_MENU)
        self.wait.until(lambda d: "recruitment" in d.current_url.lower())

    # 🔹 Actions
    def click_add(self):
        self.click(self.ADD_BUTTON)

    def enter_candidate_details(self, fname, lname, email):
        self.type(self.FIRST_NAME, fname)
        self.type(self.LAST_NAME, lname)
        self.type(self.EMAIL, email)

    def click_save(self):
        self.click(self.SAVE_BUTTON)

    # 🔹 Validations
    def is_success_message_displayed(self):
        return self.is_element_displayed(self.SUCCESS_TOAST)
