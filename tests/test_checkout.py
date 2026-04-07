import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.fixture(autouse=True)
def logged_in(driver):
    login = LoginPage(driver)
    login.open_login_page()
    login.login("standard_user", "secret_sauce")


class TestCheckout:

    def test_complete_checkout_flow(self, driver):
        """
        Full happy-path: add item → cart → fill info → finish → confirmation.
        This is the most important E2E test in the suite.
        """
        # Step 1: Add item to cart
        inventory = InventoryPage(driver)
        inventory.add_item_to_cart("sauce-labs-backpack")
        inventory.go_to_cart()

        # Step 2: Proceed to checkout
        cart = CartPage(driver)
        assert "Sauce Labs Backpack" in cart.get_cart_items()
        cart.proceed_to_checkout()

        # Step 3: Fill in customer information
        checkout = CheckoutPage(driver)
        checkout.fill_customer_info("John", "Doe", "12345")
        checkout.continue_to_overview()

        # Step 4: Verify order overview and finish
        assert "checkout-step-two" in driver.current_url
        item_total = checkout.get_item_total()
        assert "$" in item_total, "Item total should be displayed"
        checkout.finish_order()

        # Step 5: Confirm success
        assert "checkout-complete" in driver.current_url
        confirmation = checkout.get_confirmation_message()
        assert "Thank you for your order" in confirmation

    def test_checkout_with_multiple_items(self, driver):
        """Two items are both present in the checkout overview."""
        inventory = InventoryPage(driver)
        inventory.add_item_to_cart("sauce-labs-backpack")
        inventory.add_item_to_cart("sauce-labs-bike-light")
        inventory.go_to_cart()

        cart = CartPage(driver)
        assert cart.get_item_count() == 2
        cart.proceed_to_checkout()

        checkout = CheckoutPage(driver)
        checkout.fill_customer_info("Jane", "Smith", "98765")
        checkout.continue_to_overview()
        checkout.finish_order()

        assert "Thank you for your order" in checkout.get_confirmation_message()

    def test_checkout_requires_first_name(self, driver):
        """Leaving first name blank shows an error on the info page."""
        inventory = InventoryPage(driver)
        inventory.add_item_to_cart("sauce-labs-backpack")
        inventory.go_to_cart()

        CartPage(driver).proceed_to_checkout()

        checkout = CheckoutPage(driver)
        checkout.fill_customer_info("", "Doe", "12345")
        checkout.continue_to_overview()

        assert checkout.is_error_displayed()
        assert "First Name is required" in checkout.get_error_message()

    def test_checkout_requires_last_name(self, driver):
        """Leaving last name blank shows an error."""
        inventory = InventoryPage(driver)
        inventory.add_item_to_cart("sauce-labs-backpack")
        inventory.go_to_cart()

        CartPage(driver).proceed_to_checkout()

        checkout = CheckoutPage(driver)
        checkout.fill_customer_info("John", "", "12345")
        checkout.continue_to_overview()

        assert checkout.is_error_displayed()
        assert "Last Name is required" in checkout.get_error_message()

    def test_checkout_requires_zip_code(self, driver):
        """Leaving zip blank shows an error."""
        inventory = InventoryPage(driver)
        inventory.add_item_to_cart("sauce-labs-backpack")
        inventory.go_to_cart()

        CartPage(driver).proceed_to_checkout()

        checkout = CheckoutPage(driver)
        checkout.fill_customer_info("John", "Doe", "")
        checkout.continue_to_overview()

        assert checkout.is_error_displayed()
        assert "Postal Code is required" in checkout.get_error_message()


class TestLogout:

    def test_logout_redirects_to_login(self, driver):
        """Logging out lands the user back on the login page."""
        inventory = InventoryPage(driver)
        inventory.logout()

        assert driver.current_url == "https://www.saucedemo.com/"
        login = LoginPage(driver)
        assert login.is_visible(login.LOGIN_BUTTON)
