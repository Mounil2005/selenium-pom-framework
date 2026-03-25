from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    # --- Step 1: Your Information ---
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT  = (By.ID, "last-name")
    ZIP_INPUT        = (By.ID, "postal-code")
    CONTINUE_BUTTON  = (By.ID, "continue")
    ERROR_MESSAGE    = (By.CSS_SELECTOR, "[data-test='error']")

    # --- Step 2: Overview ---
    FINISH_BUTTON    = (By.ID, "finish")
    ITEM_TOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")

    # --- Step 3: Complete ---
    CONFIRMATION_HEADER = (By.CLASS_NAME, "complete-header")
    BACK_HOME_BUTTON    = (By.ID, "back-to-products")

    def fill_customer_info(self, first_name, last_name, zip_code):
        self.type(self.FIRST_NAME_INPUT, first_name)
        self.type(self.LAST_NAME_INPUT, last_name)
        self.type(self.ZIP_INPUT, zip_code)

    def continue_to_overview(self):
        self.click(self.CONTINUE_BUTTON)

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self):
        return self.is_visible(self.ERROR_MESSAGE)

    def get_item_total(self):
        """Returns the subtotal string, e.g. 'Item total: $29.99'"""
        return self.get_text(self.ITEM_TOTAL_LABEL)

    def finish_order(self):
        self.click(self.FINISH_BUTTON)

    def get_confirmation_message(self):
        return self.get_text(self.CONFIRMATION_HEADER)

    def back_to_home(self):
        self.click(self.BACK_HOME_BUTTON)
