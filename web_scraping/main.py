from config import ScraperConfig
from scraper import AmazonScraper
from storage import DataStorage
import logging

def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Initialize configuration
    config = ScraperConfig()
    
    # Initialize scraper
    scraper = AmazonScraper(config)
    
    try:
        # Login to Amazon
        if not scraper.login():
            logging.error("Failed to login. Exiting...")
            return
            
        # Scrape each category
        for category in config.CATEGORIES:
            logging.info(f"Scraping category: {category['name']}")
            scraper.scrape_category(category['url'], category['name'])
            
        # Save the results
        if scraper.products:
            DataStorage.save_to_json(scraper.products, "amazon_products.json")
            DataStorage.save_to_csv(scraper.products, "amazon_products.csv")
            logging.info(f"Successfully scraped {len(scraper.products)} products")
        else:
            logging.warning("No products were scraped")
            
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        scraper.driver.quit()

if __name__ == "__main__":
    main()