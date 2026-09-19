import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class InventoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

        # Locators
        self.menu_button = (By.ID, "react-burger-menu-btn")
        self.logout_link = (By.ID, "logout_sidebar_link")
        self.reset_link = (By.ID, "reset_sidebar_link")
        self.cart_icon = (By.CLASS_BAR, "shopping_cart_link")
        self.cart_badge = (By.CLASS_NAME, "shopping_cart_badge")
        self.inventory_items = (By.CLASS_NAME, "inventory_item")
        self.item_name = (By.CLASS_NAME, "inventory_item_name")
        self.item_price = (By.CLASS_NAME, "inventory_item_price")
        self.add_to_cart_btn = (By.XPATH, ".//button[text()='Add to cart']")
        self.sort_dropdown = (By.CLASS_NAME, "product_sort_container")

    def click_menu(self):
        self.wait.until(EC.element_to_be_clickable(self.menu_button)).click()

    def logout(self):
        self.click_menu()
        self.wait.until(EC.element_to_be_clickable(self.logout_link)).click()

    def reset_app_state(self):
        self.click_menu()
        self.wait.until(EC.element_to_be_clickable(self.reset_link)).click()
        # Close menu after reset to return to clean UI state
        self.driver.find_element(By.ID, "react-burger-cross-btn").click()

    def is_cart_icon_visible(self):
        return self.wait.until(EC.visibility_of_element_located(self.cart_icon)).is_displayed()

    def navigate_to_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.cart_icon)).click()

    def select_random_products(self, count=4):
        items = self.wait.until(EC.presence_of_all_elements_located(self.inventory_items))
        selected_indices = random.sample(range(len(items)), count)

        extracted_data = []
        for idx in selected_indices:
            # Re-fetch elements to avoid stale references
            current_items = self.driver.find_elements(*self.inventory_items)
            target_item = current_items[idx]

            name = target_item.find_element(*self.item_name).text
            price = target_item.find_element(*self.item_price).text
            extracted_data.append({"name": name, "price": price})

            target_item.find_element(*self.add_to_cart_btn).click()

        return extracted_data

    def get_cart_count(self):
        try:
            return int(self.driver.find_element(*self.cart_badge).text)
        except:
            return 0

    def sort_products_by(self, option_text):
        dropdown = Select(self.wait.until(EC.presence_of_element_located(self.sort_dropdown)))
        dropdown.select_by_visible_text(option_text)

    def get_all_product_names(self):
        items = self.wait.until(EC.presence_of_all_elements_located(self.item_name))
        return [item.text for item in items]

    def get_all_product_prices(self):
        items = self.wait.until(EC.presence_of_all_elements_located(self.item_price))
        return [float(item.text.replace('$', '')) for item in items]
