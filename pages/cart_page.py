from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    # --- Locators ---
    CART_ITEMS       = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES       = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON  = (By.ID, "checkout")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")

    def _remove_btn(self, item_data_test):
        return (By.CSS_SELECTOR, f"[data-test='remove-{item_data_test}']")

    def get_cart_items(self):
        """Returns list of item name strings currently in the cart."""
        if not self.is_visible(self.CART_ITEMS):
            return []
        return [el.text for el in self.get_all_elements(self.ITEM_NAMES)]

    def get_item_count(self):
        try:
            return len(self.get_all_elements(self.CART_ITEMS))
        except Exception:
            return 0

    def remove_item(self, item_data_test):
        self.js_click(self._remove_btn(item_data_test))

    def proceed_to_checkout(self):
        from selenium.webdriver.support import expected_conditions as EC
        self.js_click(self.CHECKOUT_BUTTON)
        self.wait.until(EC.url_contains("checkout"))

    def continue_shopping(self):
        from selenium.webdriver.support import expected_conditions as EC
        self.click(self.CONTINUE_SHOPPING)
        self.wait.until(EC.url_contains("inventory"))
