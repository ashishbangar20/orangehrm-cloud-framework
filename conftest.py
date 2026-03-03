import shutil
import os
import subprocess
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config.config import BASE_URL


# -------------------------------
# Pytest Command Line Options
# -------------------------------
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--headless", action="store", default="true")


# -------------------------------
# Browser Setup Fixture
# -------------------------------
@pytest.fixture()
def setup(request):

    browser = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless").lower() == "true"
    grid_url = os.getenv("GRID_URL")

    print("\n========== Execution Info ==========")
    print(f"Browser   : {browser}")
    print(f"Headless  : {headless}")
    print(f"GRID_URL  : {grid_url}")
    print("====================================\n")

    if browser != "chrome":
        raise ValueError("Only Chrome supported in this setup")

    options = Options()

    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    if os.path.exists("/usr/bin/chromium"):
        options.binary_location = "/usr/bin/chromium"

    driver = None

    try:
        if grid_url:
            print("Starting Remote WebDriver...")
            driver = webdriver.Remote(
                command_executor=grid_url,
                options=options
            )
        else:
            print("Starting Local Chrome WebDriver...")
            driver = webdriver.Chrome(options=options)

        driver.implicitly_wait(5)
        driver.get(BASE_URL)

        yield driver

    finally:
        if driver:
            driver.quit()


# -------------------------------
# Allure Failure Screenshot Hook
# -------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("setup")

        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )


# -------------------------------
# Auto Generate & Open Allure Report (LOCAL ONLY)
# -------------------------------
def pytest_sessionfinish(session, exitstatus):
    """
    Auto generate & open Allure report
    ONLY when running locally.
    """

    # 🔥 Strict CI check (Jenkins sets CI=true)
    if os.getenv("CI", "").lower() == "true":
        print("\nCI environment detected. Skipping Allure auto-open.\n")
        return

    results_dir = "allure-results"
    report_dir = "allure-report"

    # If Allure CLI not installed, skip safely
    if not shutil.which("allure"):
        print("\nAllure CLI not found. Skipping report auto-generation.\n")
        return

    if os.path.exists(results_dir):

        print("\nGenerating Allure report...\n")

        subprocess.run(
            ["allure", "generate", results_dir, "-o", report_dir, "--clean"],
            check=False
        )

        print("\nOpening Allure report in browser...\n")

        subprocess.run(
            ["allure", "open", report_dir],
            check=False
        )