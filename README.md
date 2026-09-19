# PAT-C-WE-E-B17-Project-3
Project-3

# SauceDemo E-Commerce Web Test Automation

This project handles automated UI validation testing for the SauceDemo mock application using Python, Selenium Webdriver, and the structural design layout patterns of the Page Object Model (POM).

## Architecture Approach
- **Page Object Model (POM)** structure encapsulates UI locators and behavioral mechanics within page abstraction layers.
- **Robust Synchronization** uses Explicit Waits (`WebDriverWait`) to handle dynamic state updates without thread sleepers.
- **Data Consistency** isolates assertions within a standardized Python test run ecosystem.

## Execution Requirements
Ensure you have Python 3.x along with Chrome web browser utilities configured on your running node environment.

1. **Install requirements:**
   ```bash
   pip install selenium
   ```
2. **Execute execution test script suite:**
   ```bash
   python -m unittest tests/test_saucedemo.py
   ```

