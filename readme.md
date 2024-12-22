# Amazon Web Scraper

## Overview

The **Amazon Web Scraper** is a Python-based tool designed to automate the login process to Amazon's website. Utilizing **Selenium WebDriver**, this scraper allows users to log in programmatically and can be extended to perform additional tasks such as product searches and data extraction.

## Features

- **Automated Login**: Seamlessly log in to Amazon accounts.
- **Error Handling**: Manage common login errors and alerts.
- **WebDriver Manager**: Automatically manage ChromeDriver installations.
- **Headless Operation**: Run the scraper in the background without a GUI.

## Requirements

To run the Amazon Web Scraper, ensure you have the following installed:

- **Python**: Version 3.6 or higher
- **Selenium**: For web automation
- **WebDriver Manager**: To manage ChromeDriver
- **Chrome Browser**: Ensure you have the latest version installed

## Setup Instructions

### Step 1: Install Python

Make sure Python is installed on your machine. You can download it from the official [Python website](https://www.python.org/downloads/).

### Step 2: Create a Virtual Environment (Optional)

Creating a virtual environment is recommended to manage dependencies. Use the following commands:
Navigate to your project directory
cd /path/to/your/project
Create a virtual environment
python -m venv venv
Activate the virtual environment
On Windows
venv\Scripts\activate
On macOS/Linux
source venv/bin/activate



### Step 3: Install Required Packages

Install the necessary packages using pip: pip install selenium webdriver-manager



### Step 4: Configure Your Scraper

1. **Create a Configuration File**: Create a file named `config.py` in your project directory and add the following code:

    ```python
    class ScraperConfig:
        LOGIN_URL = "https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2F%3Fref_%3Dnav_custrec_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0"
        USERNAME = "your_email@example.com"  # Replace with your Amazon email
        PASSWORD = "your_password"  # Replace with your Amazon password
        PAGE_LOAD_TIMEOUT = 30  # Adjust as needed
    ```

2. **Replace Placeholder Values**: Update `your_email@example.com` and `your_password` with your actual Amazon login credentials.

### Step 5: Create the Scraper Script

Create a file named `scraper.py` in your project directory and add the following code:

   from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time
class AmazonScraper:
def init(self, config):
self.config = config
self.setup_logging()
self.setup_driver()
def setup_logging(self):
logging.basicConfig(
level=logging.INFO,
format='%(asctime)s - %(levelname)s - %(message)s',
filename='scraper.log'
)
self.logger = logging.getLogger(name)
def setup_driver(self):
chrome_options = Options()
chrome_options.add_argument('--headless') # Run in headless mode (optional)
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# Use WebDriver Manager to get the ChromeDriver
self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
self.driver.implicitly_wait(20)
self.driver.set_page_load_timeout(self.config.PAGE_LOAD_TIMEOUT)
def login(self):
try:
self.driver.get(self.config.LOGIN_URL)
self.logger.info("Navigated to login page.")
self.logger.info(f"Current URL: {self.driver.current_url}")
wait = WebDriverWait(self.driver, 30)
# Wait for the email field to be present
wait.until(EC.presence_of_element_located((By.ID, "ap_email")))
self.logger.info("Email field is present.")
# Enter email
email_field = self.driver.find_element(By.ID, "ap_email")
email_field.send_keys(self.config.USERNAME)
self.driver.find_element(By.ID, "continue").click()
self.logger.info("Clicked continue button.")
# Check for email missing or invalid alerts
try:
wait.until(EC.visibility_of_element_located((By.ID, "auth-email-missing-alert")))
self.logger.error("Email is missing. Please enter a valid email.")
return False
except TimeoutException:
self.logger.info("No missing email alert detected.")
try:
wait.until(EC.visibility_of_element_located((By.ID, "auth-email-invalid-claim-alert")))
self.logger.error("Invalid email address. Please correct and try again.")
return False
except TimeoutException:
self.logger.info("No invalid email alert detected.")
# Wait for the password field to be present and visible
wait.until(EC.visibility_of_element_located((By.ID, "ap-credential-autofill-hint")))
self.logger.info("Password field is present.")
# Use JavaScript to focus on the password field
password_field = self.driver.find_element(By.ID, "ap-credential-autofill-hint")
self.driver.execute_script("arguments[0].focus();", password_field) # Focus on the password field
password_field.send_keys(self.config.PASSWORD)
self.driver.find_element(By.ID, "signInSubmit").click()
self.logger.info("Login attempt submitted.")
# Check for login success or failure
wait.until(EC.presence_of_element_located((By.ID, "some_element_that_only_appears_when_logged_in"))) # Replace with an actual element ID
self.logger.info("Login successful.")
return True
except Exception as e:
self.logger.error(f"Login failed: {str(e)}")
return False
if name == "main":
config = ScraperConfig()
scraper = AmazonScraper(config)
scraper.login()



### Step 6: Run the Scraper

To run the scraper, execute the following command in your terminal:python scraper.py




## Usage Guidelines

- **Headless Mode**: The scraper runs in headless mode by default. If you want to see the browser actions, you can comment out the line `chrome_options.add_argument('--headless')` in the `setup_driver` method.
- **Logging**: The scraper logs important actions and errors to `scraper.log`. Check this file for detailed information about the scraper's execution.
- **Error Handling**: The scraper includes basic error handling for login failures. If the login fails, check the log file for specific error messages.

## Important Notes

- **CAPTCHA**: If Amazon detects unusual activity, it may present a CAPTCHA challenge. The scraper will not be able to bypass CAPTCHA, and you may need to log in manually.
- **Account Security**: Be cautious when using automated scripts with your Amazon account. Ensure that you comply with Amazon's terms of service.

---

This version of the `README.md` file is structured for better readability and includes clear sections with headings, bullet points, and code blocks. You can copy and paste this content into your `README.md` file in your project directory. If you have any further modifications or requests, feel free to ask!
