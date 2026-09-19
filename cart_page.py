from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

        # Locators
        self.cart_items = (By.CLASS_NAME, "cart_item")
        self.item_name = (By.CLASS_NAME, "inventory_item_name")
        self.item_price = (By.CLASS_NAME, "inventory_item_price")
        self.checkout_button = (By.ID, "checkout")

    def get_cart_items_details(self):
        items = self.wait.until(EC.presence_of_all_elements_located(self.cart_items))
        cart_data = []
        for item in items:
            name = item.find_element(*self.item_name).text
            price = item.find_element(*self.item_price).text
            cart_data.append({"name": name, "price": price})
        return cart_data

    def proceed_to_checkout(self):
        self.wait.until(EC.element_to_be_clickable(self.checkout_button)).click()
