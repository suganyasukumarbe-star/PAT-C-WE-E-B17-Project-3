from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

        # Locators
        self.first_name = (By.ID, "first-name")
        self.last_name = (By.ID, "last-name")
        self.postal_code = (By.ID, "postal-code")
        self.continue_button = (By.ID, "continue")
        self.finish_button = (By.ID, "finish")
        self.confirmation_header = (By.CLASS_NAME, "complete-header")

    def fill_user_details(self, fname, lname, zip_code):
        self.wait.until(EC.visibility_of_element_located(self.first_name)).send_keys(fname)
        self.driver.find_element(*self.last_name).send_keys(lname)
        self.driver.find_element(*self.postal_code).send_keys(zip_code)
        self.driver.find_element(*self.continue_button).click()

    def finalize_order(self):
        self.wait.until(EC.element_to_be_clickable(self.finish_button)).click()

    def get_confirmation_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.confirmation_header)).text
