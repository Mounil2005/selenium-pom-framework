from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException


class BasePage:
    """
    All page classes inherit from here.
    Wraps Selenium calls with explicit waits so tests are stable.
    """

    BASE_URL = "https://www.saucedemo.com"
    DEFAULT_TIMEOUT = 10

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    def open(self, path=""):
        self.driver.get(self.BASE_URL + path)

    def find(self, locator):
        """Wait for element to be present and return it."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_clickable(self, locator):
        """Wait for element to be clickable and return it."""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        self.find_clickable(locator).click()

    def js_click(self, locator):
        """JavaScript click — bypasses overlay/animation issues in headless Chrome."""
        element = self.find(locator)
        self.driver.execute_script("arguments[0].click()", element)

    def type(self, locator, text):
        element = self.find_clickable(locator)
        # Use native value setter so React's onChange fires correctly.
        # element.clear() and keyboard Ctrl+A both fail to update React's
        # internal state on saucedemo's controlled inputs.
        self.driver.execute_script(
            "var setter = Object.getOwnPropertyDescriptor("
            "window.HTMLInputElement.prototype, 'value').set;"
            "setter.call(arguments[0], arguments[1]);"
            "arguments[0].dispatchEvent(new Event('input', {bubbles:true}));",
            element, text
        )

    def get_text(self, locator):
        return self.find(locator).text

    def is_visible(self, locator):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def select_dropdown_by_value(self, locator, value):
        element = self.find(locator)
        Select(element).select_by_value(value)

    def get_all_elements(self, locator):
        self.find(locator)  # wait for at least one
        return self.driver.find_elements(*locator)

    def take_screenshot(self, name):
        self.driver.save_screenshot(f"screenshots/{name}.png")

    @property
    def current_url(self):
        return self.driver.current_url

    @property
    def title(self):
        return self.driver.title
