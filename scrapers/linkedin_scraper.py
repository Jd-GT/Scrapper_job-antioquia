"""
LinkedIn Scraper with Authentication
Uses Selenium for browser automation - runs in visible mode (not headless)
Based on the working implementation from Job_auto project
"""

import logging
import time
from typing import List, Optional
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

from data_schema import JobPosting
from scrapers.base_scraper import BaseScraper

logger = logging.getLogger(__name__)

LINKEDIN_EMAIL = "tu_email@email.com"
LINKEDIN_PASSWORD = "tu_password"

LINKEDIN_BASE_URL = "https://www.linkedin.com/jobs/search/"

MAX_PAGES = 2
SCROLL_PAUSE = 3
PAGE_LOAD_WAIT = 10

LOCATIONS = [
    ("medellin", "Medellín"),
    ("envigado", "Envigado"),
    ("itagui", "Itagüí"),
    ("bello", "Bello"),
    ("rionegro", "Rionegro"),
]

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


class LinkedInScraper(BaseScraper):
    def __init__(self):
        super().__init__("LinkedIn")
        self.logged_in = False
        self.driver = None

    def _setup_driver(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        # NOT headless - this is the key!
        # options.add_argument("--headless")
        
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--log-level=3")
        
        return webdriver.Chrome(options=options)

    def _build_url(self, keyword: str, location: str) -> str:
        params = {
            "keywords": quote_plus(keyword),
            "location": quote_plus(location),
            "f_TPR": "r86400",  # Last 24 hours
            "position": "1",
            "pageNum": "0",
        }
        url = LINKEDIN_BASE_URL + "?"
        url += "&".join([f"{k}={v}" for k, v in params.items()])
        return url

    def _scroll_page(self, max_scrolls: int = 5):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scrolls = 0
        
        while scrolls < max_scrolls:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE)
            
            try:
                show_more = self.driver.find_element(
                    By.CSS_SELECTOR, 
                    "button.infinite-scroller__show-more-button"
                )
                if show_more.is_displayed():
                    show_more.click()
                    time.sleep(SCROLL_PAUSE)
            except NoSuchElementException:
                pass
            
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            scrolls += 1

    def _parse_job(self, card) -> Optional[JobPosting]:
        try:
            link = card.find("a", class_="base-card__full-link")
            if not link:
                return None
                
            url = link.get("href", "").strip()
            title_span = link.find("span", class_="sr-only")
            title = self.clean_text(title_span.text) if title_span else None
            
            if not title:
                return None
            
            company_tag = card.find("h4", class_="base-search-card__subtitle")
            company_link = company_tag.find("a") if company_tag else None
            company = self.clean_text(company_link.text) if company_link else "No especificada"
            
            location_tag = card.find("span", class_="job-search-card__location")
            location = self.clean_text(location_tag.text) if location_tag else ""
            
            date_tag = card.find("time", class_="job-search-card__listdate")
            if not date_tag:
                date_tag = card.find("time", class_="job-search-card__listdate--new")
            published = self.clean_text(date_tag.text) if date_tag else None
            
            benefit_tag = card.find("span", class_="job-posting-benefits__text")
            salary = self.clean_text(benefit_tag.text) if benefit_tag else ""
            
            return JobPosting(
                title=title,
                company=company,
                location=location,
                salary_raw=salary,
                url=url,
                source="LinkedIn",
                date_posted=published,
            )
            
        except Exception as e:
            logger.debug(f"Error parsing job: {e}")
            return None

    def get_urls(self) -> List[str]:
        urls = []
        for slug, city in LOCATIONS[:1]:  # Start with just medellin
            url = self._build_url("python", f"{slug}, Antioquia, Colombia")
            urls.append(url)
        return urls

    def parse_listings(self, soup: BeautifulSoup, url: str) -> List[JobPosting]:
        jobs: List[JobPosting] = []
        cards = soup.find_all("div", class_="base-card")
        
        logger.info(f"LinkedIn: Found {len(cards)} job cards")
        
        for card in cards:
            job = self._parse_job(card)
            if job:
                jobs.append(job)
        
        return jobs

    def _login_to_linkedin(self, driver) -> bool:
        if not SELENIUM_AVAILABLE:
            logger.error("Selenium not installed")
            return False
            
        try:
            logger.info("Opening LinkedIn login page...")
            driver.get("https://www.linkedin.com/login")
            time.sleep(3)
            
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_input.send_keys(LINKEDIN_EMAIL)
            
            password_input = driver.find_element(By.ID, "password")
            password_input.send_keys(LINKEDIN_PASSWORD)
            
            login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            time.sleep(5)
            
            if "feed" in driver.current_url or "login" not in driver.current_url:
                logger.info("Successfully logged in to LinkedIn!")
                self.logged_in = True
                return True
            else:
                logger.warning("Login may have failed")
                return False
                
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False

    def run_with_selenium(self) -> List[JobPosting]:
        if not SELENIUM_AVAILABLE:
            logger.error("Selenium not installed")
            return []
            
        all_jobs = []
        
        try:
            self.driver = self._setup_driver()
            
            if not self._login_to_linkedin(self.driver):
                self.driver.quit()
                return []
            
            urls = self.get_urls()
            
            for i, url in enumerate(urls):
                logger.info(f"LinkedIn: Scraping page {i+1}/{len(urls)}")
                
                try:
                    self.driver.get(url)
                    
                    try:
                        WebDriverWait(self.driver, PAGE_LOAD_WAIT).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "base-card"))
                        )
                    except TimeoutException:
                        logger.warning(f"Timeout waiting for results on page {i+1}")
                        continue
                    
                    self._scroll_page(max_scrolls=MAX_PAGES * 2)
                    
                    soup = BeautifulSoup(self.driver.page_source, "html.parser")
                    jobs = self.parse_listings(soup, url)
                    all_jobs.extend(jobs)
                    logger.info(f"LinkedIn: Found {len(jobs)} jobs on page {i+1}")
                    
                except Exception as e:
                    logger.warning(f"Error on page {i+1}: {e}")
                    
            self.driver.quit()
            self.driver = None
            
        except Exception as e:
            logger.error(f"Selenium error: {e}")
            if self.driver:
                self.driver.quit()
                
        logger.info(f"LinkedIn: Total jobs: {len(all_jobs)}")
        return all_jobs

    def run(self) -> List[JobPosting]:
        if SELENIUM_AVAILABLE:
            logger.info("Running LinkedIn scraper with Selenium (non-headless)...")
            return self.run_with_selenium()
        else:
            logger.warning("Selenium not available, skipping LinkedIn")
            return []
