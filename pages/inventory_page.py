from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InventoryPage(BasePage):
    # --- Locators ---
    PAGE_TITLE        = (By.CLASS_NAME, "title")
    INVENTORY_ITEMS   = (By.CLASS_NAME, "inventory_item")
    ITEM_NAMES        = (By.CLASS_NAME, "inventory_item_name")
    CART_BADGE        = (By.CLASS_NAME, "shopping_cart_badge")
    CART_ICON         = (By.CLASS_NAME, "shopping_cart_link")
    SORT_DROPDOWN     = (By.CLASS_NAME, "product_sort_container")
    BURGER_MENU       = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK       = (By.ID, "logout_sidebar_link")

    # Dynamic locator helpers — built at call time so we target specific items
    def _add_to_cart_btn(self, item_data_test):
        return (By.CSS_SELECTOR, f"[data-test='add-to-cart-{item_data_test}']")

    def _remove_btn(self, item_data_test):
        return (By.CSS_SELECTOR, f"[data-test='remove-{item_data_test}']")

    def get_page_title(self):
        return self.get_text(self.PAGE_TITLE)

    def add_item_to_cart(self, item_data_test):
        """
        item_data_test is the slug used in data-test attributes.
        e.g. 'sauce-labs-backpack'
        """
        self.click(self._add_to_cart_btn(item_data_test))

    def remove_item_from_inventory(self, item_data_test):
        self.click(self._remove_btn(item_data_test))

    def get_cart_count(self):
        if not self.is_visible(self.CART_BADGE):
            return 0
        return int(self.get_text(self.CART_BADGE))

    def go_to_cart(self):
        self.click(self.CART_ICON)

    def sort_products(self, option):
        """
        option values: 'az', 'za', 'lohi', 'hilo'
        """
        self.select_dropdown_by_value(self.SORT_DROPDOWN, option)

    def get_product_names(self):
        elements = self.get_all_elements(self.ITEM_NAMES)
        return [el.text for el in elements]

    def logout(self):
        self.click(self.BURGER_MENU)
        self.click(self.LOGOUT_LINK)
