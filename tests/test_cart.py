import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


@pytest.fixture(autouse=True)
def logged_in(driver):
    login = LoginPage(driver)
    login.open_login_page()
    login.login("standard_user", "secret_sauce")


class TestCart:

    def test_cart_shows_added_item(self, driver):
        """Item added from inventory appears in the cart."""
        inventory = InventoryPage(driver)
        inventory.add_item_to_cart("sauce-labs-backpack")
        inventory.go_to_cart()

        cart = CartPage(driver)
        assert "Sauce Labs Backpack" in cart.get_cart_items()

    def test_remove_item_from_cart(self, driver):
        """Removing an item from the cart clears it."""
        inventory = InventoryPage(driver)
        inventory.add_item_to_cart("sauce-labs-backpack")
        inventory.go_to_cart()

        cart = CartPage(driver)
        cart.remove_item("sauce-labs-backpack")

        assert cart.get_item_count() == 0

    def test_multiple_items_in_cart(self, driver):
        """All added items appear in the cart."""
        inventory = InventoryPage(driver)
        inventory.add_item_to_cart("sauce-labs-backpack")
        inventory.add_item_to_cart("sauce-labs-fleece-jacket")
        inventory.go_to_cart()

        cart = CartPage(driver)
        items = cart.get_cart_items()
        assert "Sauce Labs Backpack" in items
        assert "Sauce Labs Fleece Jacket" in items
        assert cart.get_item_count() == 2

    def test_continue_shopping_returns_to_inventory(self, driver):
        """'Continue Shopping' button takes the user back to the inventory."""
        inventory = InventoryPage(driver)
        inventory.go_to_cart()

        cart = CartPage(driver)
        cart.continue_shopping()

        assert "inventory" in driver.current_url
