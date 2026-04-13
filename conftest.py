import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def pytest_addoption(parser):
    """Adds --headless flag to the pytest CLI."""
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run Chrome in headless mode (no visible browser window)",
    )


@pytest.fixture(scope="function")
def driver(request):
    """
    Provides a Selenium WebDriver instance for each test.
    Scope='function' means a fresh browser per test — full isolation.
    """
    headless = request.config.getoption("--headless")

    options = Options()
    if headless:
        options.add_argument("--headless=new")      # Chrome >= 112 headless mode
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.implicitly_wait(0)   # we use explicit waits in BasePage — don't mix both

    yield driver                # test runs here

    # Teardown: capture screenshot on failure, then quit
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        driver.save_screenshot(f"screenshots/{request.node.name}.png")

    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attaches test result to the request node so the fixture can read it."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
