# Selenium Automated Test Suite

![Selenium Tests](https://github.com/Mounil2005/selenium-pom-framework/actions/workflows/tests.yml/badge.svg)

End-to-end UI test suite for [SauceDemo](https://www.saucedemo.com) built with Python, Selenium 4, and pytest. Demonstrates the **Page Object Model (POM)** design pattern, explicit waits, headless execution, and automated HTML reporting.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10+ | Language |
| Selenium 4 | Browser automation |
| pytest | Test runner & assertions |
| webdriver-manager | Auto-downloads matching ChromeDriver |
| pytest-html | Visual HTML test reports |

---

## Project Structure

```
selenium-test-suite/
├── pages/              # Page Object Model classes
│   ├── base_page.py    # Shared Selenium helpers with explicit waits
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/              # pytest test cases
│   ├── test_login.py
│   ├── test_inventory.py
│   ├── test_cart.py
│   └── test_checkout.py
├── reports/            # Generated HTML reports
├── screenshots/        # Auto-captured on test failure
├── conftest.py         # pytest fixtures (browser setup/teardown)
├── pytest.ini          # pytest configuration
└── requirements.txt
```

---

## Prerequisites

- Python 3.10 or higher
- Google Chrome installed

---

## Setup

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd selenium-test-suite

# 2. Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Running the Tests

```bash
# Run all tests (opens visible Chrome window)
pytest

# Run in headless mode (no browser window — great for CI)
pytest --headless

# Run a specific test file
pytest tests/test_login.py

# Run a specific test by name
pytest tests/test_checkout.py::TestCheckout::test_complete_checkout_flow

# Run with extra verbosity
pytest -v --headless

# Run and stop after first failure
pytest -x
```

All runs automatically generate `reports/report.html`.

---

## Viewing the HTML Report

After running tests, open the report in your browser:

```bash
# Windows
start reports/report.html

# macOS
open reports/report.html

# Linux
xdg-open reports/report.html
```

The report shows pass/fail status, test durations, and captured logs for each test.

---

## Test Coverage

| Test File | Scenarios |
|---|---|
| `test_login.py` | Valid login, invalid credentials, locked-out user, empty field validation |
| `test_inventory.py` | Add to cart, remove from inventory page, all 4 sort options (A-Z, Z-A, price low-high, price high-low) |
| `test_cart.py` | Cart contents, remove item, multi-item cart, continue shopping navigation |
| `test_checkout.py` | Full E2E checkout flow, multi-item checkout, required field validation, logout |

---

## Design Decisions

**Page Object Model:** Each page is a Python class. Locators and actions live inside the class — tests only call methods, never raw Selenium. This means a locator change only needs to be updated in one place.

**Explicit Waits:** `BasePage` uses `WebDriverWait` instead of `time.sleep()`. Tests wait only as long as needed, making the suite faster and more reliable.

**Headless Flag:** The `--headless` CLI option is registered in `conftest.py`, so no code changes are needed to switch between visible and headless execution.

**Failure Screenshots:** `conftest.py` hooks into pytest's result reporting. If a test fails, a screenshot is saved to `screenshots/<test_name>.png` automatically.
