import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@pytest.fixture(autouse=True)
def logged_in(driver):
    """Log in before each test in this module."""
    login = LoginPage(driver)
    login.open_login_page()
    login.login("standard_user", "secret_sauce")


class TestInventory:

    def test_add_single_item_to_cart(self, driver):
        """Cart badge shows 1 after adding one item."""
        inventory = InventoryPage(driver)
        inventory.add_item_to_cart("sauce-labs-backpack")

        assert inventory.get_cart_count() == 1

    def test_add_multiple_items_to_cart(self, driver):
        """Cart badge updates correctly for multiple items."""
        inventory = InventoryPage(driver)
        inventory.add_item_to_cart("sauce-labs-backpack")
        inventory.add_item_to_cart("sauce-labs-bike-light")

        assert inventory.get_cart_count() == 2

    def test_remove_item_from_inventory_page(self, driver):
        """After removing the item the cart badge disappears."""
        inventory = InventoryPage(driver)
        inventory.add_item_to_cart("sauce-labs-backpack")
        assert inventory.get_cart_count() == 1

        inventory.remove_item_from_inventory("sauce-labs-backpack")
        assert inventory.get_cart_count() == 0

    def test_sort_products_a_to_z(self, driver):
        """Default sort is A→Z; names should already be alphabetically sorted."""
        inventory = InventoryPage(driver)
        inventory.sort_products("az")
        names = inventory.get_product_names()

        assert names == sorted(names), "Products should be in A→Z order"

    def test_sort_products_z_to_a(self, driver):
        """Z→A sort reverses the alphabetical order."""
        inventory = InventoryPage(driver)
        inventory.sort_products("za")
        names = inventory.get_product_names()

        assert names == sorted(names, reverse=True), "Products should be in Z→A order"

    def test_sort_products_low_to_high(self, driver):
        """Low→High sort orders items by ascending price."""
        from selenium.webdriver.common.by import By

        inventory = InventoryPage(driver)
        inventory.sort_products("lohi")

        price_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        prices = [float(el.text.replace("$", "")) for el in price_elements]

        assert prices == sorted(prices), "Prices should be in ascending order"

    def test_sort_products_high_to_low(self, driver):
        """High→Low sort orders items by descending price."""
        from selenium.webdriver.common.by import By

        inventory = InventoryPage(driver)
        inventory.sort_products("hilo")

        price_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        prices = [float(el.text.replace("$", "")) for el in price_elements]

        assert prices == sorted(prices, reverse=True), "Prices should be in descending order"
