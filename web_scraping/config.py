from dataclasses import dataclass

@dataclass
class ScraperConfig:
    # Amazon credentials
    
    USERNAME: str = "karanbaloni@gmail.com"
    PASSWORD: str = "@Shri69*"
    
    # URLs
    BASE_URL: str = "https://www.amazon.in"
    LOGIN_URL: str = "https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2F%3Fref_%3Dnav_custrec_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0"
    BESTSELLER_URL: str = "https://www.amazon.in/gp/bestsellers/"
    
    # Scraping parameters
    MAX_PRODUCTS_PER_CATEGORY: int = 1500
    MIN_DISCOUNT_PERCENTAGE: int = 50
    
    # Categories to scrape
    CATEGORIES = [
        {"name": "Kitchen", "url": "https://www.amazon.in/gp/bestsellers/kitchen/"},
        {"name": "Shoes", "url": "https://www.amazon.in/gp/bestsellers/shoes/"},
        {"name": "Computers", "url": "https://www.amazon.in/gp/bestsellers/computers/"},
        {"name": "Electronics", "url": "https://www.amazon.in/gp/bestsellers/electronics/"},
        # Add more categories as needed
    ]
    
    # Selenium settings
    IMPLICIT_WAIT: int = 10
    PAGE_LOAD_TIMEOUT: int = 30 