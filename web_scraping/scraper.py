from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
import csv
import logging
from typing import List, Optional
import time

from config import ScraperConfig
from models import Product

class AmazonScraper:
    def __init__(self, config: ScraperConfig):
        self.config = config
        self.setup_logging()
        self.setup_driver()
        self.products: List[Product] = []
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='scraper.log'
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        self.driver.implicitly_wait(20)
        self.driver.set_page_load_timeout(self.config.PAGE_LOAD_TIMEOUT)
        
    def login(self):
        try:
            self.driver.get(self.config.LOGIN_URL)
            self.logger.info("Navigated to login page.")
            self.logger.info(f"Current URL: {self.driver.current_url}")  # Log the current URL

            wait = WebDriverWait(self.driver, 30)  # Increase wait time

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

            # Wait for the password field to be present
            wait.until(EC.presence_of_element_located((By.ID, "ap-credential-autofill-hint")))
            self.logger.info("Password field is present.")

            # Enter password
            password_field = self.driver.find_element(By.ID, "ap-credential-autofill-hint")
            password_field.send_keys(self.config.PASSWORD)
            self.driver.find_element(By.ID, "signInSubmit").click()
            self.logger.info("Login attempt submitted.")

            # Check for login success or failure
            # You can check for a specific element that appears only when logged in
            wait.until(EC.presence_of_element_located((By.ID, "some_element_that_only_appears_when_logged_in")))  # Replace with an actual element ID
            self.logger.info("Login successful.")
            return True
        except Exception as e:
            self.logger.error(f"Login failed: {str(e)}")
            return False
            
    def extract_product_details(self, product_element, category: str) -> Optional[Product]:
        try:
            # Extract basic product information
            name = product_element.find_element(By.CSS_SELECTOR, "span.a-text-normal").text
            
            # Extract price information
            price_element = product_element.find_element(By.CSS_SELECTOR, "span.a-price-whole")
            price = float(price_element.text.replace(",", ""))
            
            # Extract discount information
            discount_element = product_element.find_element(By.CSS_SELECTOR, "span.a-text-price")
            original_price = float(discount_element.text.replace("₹", "").replace(",", ""))
            discount = ((original_price - price) / original_price) * 100
            
            # Skip if discount is less than minimum required
            if discount < self.config.MIN_DISCOUNT_PERCENTAGE:
                return None
                
            # Extract other details
            product = Product(
                name=name,
                price=price,
                original_price=original_price,
                discount=discount,
                best_seller_rank=self._extract_rank(product_element),
                ship_from=self._extract_ship_from(product_element),
                sold_by=self._extract_sold_by(product_element),
                rating=self._extract_rating(product_element),
                description=self._extract_description(product_element),
                monthly_purchases=self._extract_monthly_purchases(product_element),
                category=category,
                images=self._extract_images(product_element)
            )
            
            return product
        except Exception as e:
            self.logger.error(f"Error extracting product details: {str(e)}")
            return None
            
    def scrape_category(self, category_url: str, category_name: str):
        try:
            self.driver.get(category_url)
            products_scraped = 0
            page = 1
            
            while products_scraped < self.config.MAX_PRODUCTS_PER_CATEGORY:
                product_elements = self.driver.find_elements(
                    By.CSS_SELECTOR, 
                    "div.a-section.a-spacing-none.p13n-asin"
                )
                
                for element in product_elements:
                    product = self.extract_product_details(element, category_name)
                    if product:
                        self.products.append(product)
                        products_scraped += 1
                        
                    if products_scraped >= self.config.MAX_PRODUCTS_PER_CATEGORY:
                        break
                        
                # Try to go to next page
                try:
                    next_button = self.driver.find_element(By.CSS_SELECTOR, "li.a-last a")
                    next_button.click()
                    page += 1
                    time.sleep(2)  # Prevent too many requests
                except NoSuchElementException:
                    break
                    
        except Exception as e:
            self.logger.error(f"Error scraping category {category_name}: {str(e)}") 