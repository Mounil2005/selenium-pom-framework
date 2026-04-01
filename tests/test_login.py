import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


VALID_USER     = "standard_user"
VALID_PASS     = "secret_sauce"
INVALID_USER   = "wrong_user"
INVALID_PASS   = "wrong_pass"
LOCKED_USER    = "locked_out_user"


class TestLogin:

    def test_valid_login(self, driver):
        """User with correct credentials reaches the inventory page."""
        login = LoginPage(driver)
        login.open_login_page()
        login.login(VALID_USER, VALID_PASS)

        inventory = InventoryPage(driver)
        assert "inventory" in driver.current_url
        assert inventory.get_page_title() == "Products"

    def test_invalid_credentials_show_error(self, driver):
        """Wrong credentials display an error message — no redirect."""
        login = LoginPage(driver)
        login.open_login_page()
        login.login(INVALID_USER, INVALID_PASS)

        assert login.is_error_displayed(), "Error message should be visible"
        assert "Epic sadface" in login.get_error_message()
        assert "inventory" not in driver.current_url

    def test_locked_out_user_shows_error(self, driver):
        """Locked-out account is rejected with a specific message."""
        login = LoginPage(driver)
        login.open_login_page()
        login.login(LOCKED_USER, VALID_PASS)

        assert login.is_error_displayed()
        assert "locked out" in login.get_error_message().lower()

    def test_empty_username_shows_error(self, driver):
        """Submitting without a username shows a validation error."""
        login = LoginPage(driver)
        login.open_login_page()
        login.login("", VALID_PASS)

        assert login.is_error_displayed()
        assert "Username is required" in login.get_error_message()

    def test_empty_password_shows_error(self, driver):
        """Submitting without a password shows a validation error."""
        login = LoginPage(driver)
        login.open_login_page()
        login.login(VALID_USER, "")

        assert login.is_error_displayed()
        assert "Password is required" in login.get_error_message()
