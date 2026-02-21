import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config.config import BASE_URL


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--headless", action="store", default="true")


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
        raise ValueError("Only Chrome supported in cloud mode")

    options = Options()

    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    if os.path.exists("/usr/bin/chromium"):
        options.binary_location = "/usr/bin/chromium"

    driver = (
        webdriver.Remote(command_executor=grid_url, options=options)
        if grid_url else
        webdriver.Chrome(options=options)
    )

    driver.implicitly_wait(5)
    driver.get(BASE_URL)

    yield driver
    driver.quit()