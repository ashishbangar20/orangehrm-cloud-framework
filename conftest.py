import shutil
import os
import subprocess
import pytest
import allure

from selenium import webdriver

# Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Edge
from selenium.webdriver.edge.options import Options as EdgeOptions

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

    print("\n========== Execution Info ==========")
    print(f"Browser   : {browser}")
    print(f"Headless  : {headless}")
    print("====================================\n")

    driver = None

    try:
        # -------------------------------
        # CHROME
        # -------------------------------
        if browser == "chrome":
            options = ChromeOptions()

            if headless:
                options.add_argument("--headless=new")

            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")

            if os.path.exists("/usr/bin/chromium"):
                options.binary_location = "/usr/bin/chromium"

            print("Starting Chrome...")
            driver = webdriver.Chrome(options=options)

        # -------------------------------
        # FIREFOX
        # -------------------------------
        elif browser == "firefox":
            options = FirefoxOptions()

            if headless:
                options.add_argument("--headless")

            print("Starting Firefox...")
            driver = webdriver.Firefox(options=options)

        # -------------------------------
        # EDGE
        # -------------------------------
        elif browser == "edge":
            options = EdgeOptions()

            if headless:
                options.add_argument("--headless=new")

            print("Starting Edge...")
            driver = webdriver.Edge(options=options)

        else:
            raise ValueError("Unsupported browser! Use chrome/firefox/edge")

        driver.maximize_window()
        driver.get(BASE_URL)

        yield driver

    finally:
        if driver:
            driver.quit()


# -------------------------------
# Allure Failure Screenshot Hook
# -------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
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

    if os.getenv("CI", "").lower() == "true":
        print("\nCI environment detected. Skipping Allure auto-open.\n")
        return

    results_dir = "allure-results"
    report_dir = "allure-report"

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