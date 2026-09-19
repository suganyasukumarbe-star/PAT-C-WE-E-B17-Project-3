import os
import unittest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


class TestSauceDemo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initializing the Chrome Driver configuration
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        cls.driver = webdriver.Chrome(options=options)

        # Instantiate Page Objects
        cls.login_page = LoginPage(cls.driver)
        cls.inventory_page = InventoryPage(cls.driver)
        cls.cart_page = CartPage(cls.driver)
        cls.checkout_page = CheckoutPage(cls.driver)

        # Global variable storage for data handoff between test cases
        cls.selected_products = []

    def test_01_login_valid_user(self):
        """Test Case 1: Login with various predefined users"""
        self.login_page.open()
        self.login_page.login("standard_user", "secret_sauce")
        self.assertTrue(self.inventory_page.is_cart_icon_visible(), "Login failed for valid user context.")

    def test_02_validate_logout(self):
        """Test Case 3: Validate logout functionality"""
        # Executing TC-3 out of initial sequential order to check system lifecycle early
        self.inventory_page.logout()
        self.assertTrue(self.login_page.is_on_login_page(), "Logout action failed to redirect to landing interface.")

    def test_03_login_invalid_user(self):
        """Test Case 2: Login with invalid credentials"""
        self.login_page.open()
        self.login_page.login("invalid_user", "wrong_password")
        error_text = self.login_page.get_error_message()
        self.assertIn("Username and password do not match", error_text,
                      "Error banner mismatch for invalid credentials.")

    def test_04_cart_icon_visibility(self):
        """Test Case 4: Check cart icon visibility"""
        self.login_page.open()
        self.login_page.login("standard_user", "secret_sauce")
        self.assertTrue(self.inventory_page.is_cart_icon_visible(), "Cart icon container missing post landing.")

    def test_05_random_product_selection(self):
        """Test Case 5: Random selection of products and data extraction"""
        TestSauceDemo.selected_products = self.inventory_page.select_random_products(count=4)
        self.assertEqual(len(TestSauceDemo.selected_products), 4, "Failed to capture data matrices for 4 items.")
        print(f"\n[Data Extracted] Chosen Products: {TestSauceDemo.selected_products}")

    def test_06_validate_cart_count(self):
        """Test Case 6: Add selected products to cart and validate"""
        # Step handling relies on the execution sequence from test_05
        count = self.inventory_page.get_cart_count()
        self.assertEqual(count, 4, f"Expected 4 items in cart badge tracking array, found {count}.")

    def test_07_validate_cart_details(self):
        """Test Case 7: Validate product details inside the cart"""
        self.inventory_page.navigate_to_cart()
        cart_items = self.cart_page.get_cart_items_details()

        # Verify names and values match selections made in TC-5
        for item in TestSauceDemo.selected_products:
            self.assertIn(item, cart_items, f"Selected entry {item} missing or inaccurate in active cart instance.")

    def test_08_complete_checkout(self):
        """Test Case 8: Complete checkout and validate order"""
        self.cart_page.proceed_to_checkout()

        # Performance path capture validation via screenshot framework
        os.makedirs("screenshots", exist_ok=True)
        self.checkout_page.fill_user_details("QA", "Engineer", "600001")
        self.driver.save_screenshot("screenshots/order_summary.png")

        self.checkout_page.finalize_order()
        conf_msg = self.checkout_page.get_confirmation_message()
        self.assertEqual(conf_msg, "Thank you for your order!", "Final checkout processing failed.")

    def test_09_sorting_functionality(self):
        """Test Case 9: Validate sorting functionality on the products page"""
        # Return to core inventory environment
        self.driver.get("https://saucedemo.com")

        # Test Price High to Low Sorting
        self.inventory_page.sort_products_by("Price (low to high)")
        prices = self.inventory_page.get_all_product_prices()
        self.assertEqual(prices, sorted(prices), "Pricing sequence structure failed ascending verification step.")

        # Test Name Z to A Sorting
        self.inventory_page.sort_products_by("Name (Z to A)")
        names = self.inventory_page.get_all_product_names()
        self.assertEqual(names, sorted(names, reverse=True), "Alphabetical array failed descending verification step.")

    def test_10_reset_app_state(self):
        """Test Case 10: Validate 'Reset App State' functionality"""
        # Re-add items to test reset operations
        self.inventory_page.select_random_products(count=2)
        self.assertTrue(self.inventory_page.get_cart_count() > 0,
                        "Failed to load buffer array items for system reset test.")

        # Execution of reset operational hook
        self.inventory_page.reset_app_state()
        self.driver.refresh()  # Refresh browser to confirm state storage flush

        final_count = self.inventory_page.get_cart_count()
        self.assertEqual(final_count, 0, f"App state operational reset failed. Current item tally: {final_count}")

    @classmethod
    def tearDownClass(cls):
        # Gracefully close active instances
        if cls.driver:
            cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
