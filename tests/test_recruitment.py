import pytest
import allure
import time
from pages.login_page import LoginPage
from pages.recruitment_page import RecruitmentPage


@allure.feature("Recruitment Module")
class TestRecruitment:

    @pytest.mark.smoke
    @allure.story("Add Candidate Positive")
    def test_add_candidate(self, setup):

        driver = setup
        login = LoginPage(driver)
        recruitment = RecruitmentPage(driver)

        # ✅ Correct Data
        fname = "Ashish"
        lname = "Bangar"
        full_name = f"{fname} {lname}"   # 🔥 FIXED
        email = f"ashish{int(time.time())}@test.com"

        with allure.step("Login to application"):
            login.login("Admin", "admin123")

        with allure.step("Navigate to Recruitment module"):
            recruitment.go_to_recruitment()

        with allure.step("Click Add button"):
            recruitment.click_add()

        with allure.step("Enter candidate details"):
            recruitment.enter_candidate_details(fname, lname, email)

        with allure.step("Click Save"):
            recruitment.click_save()

        with allure.step("Verify success message"):
            assert recruitment.is_success_message_displayed(), "Candidate not created"

