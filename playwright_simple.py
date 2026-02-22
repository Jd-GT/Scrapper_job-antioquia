"""
Simplified Playwright scraper - focusing on working platforms
"""

import logging
import asyncio
from bs4 import BeautifulSoup

from data_schema import JobPosting

logger = logging.getLogger(__name__)

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


LOCATIONS = [
    ("medellin", "Medellín"),
    ("envigado", "Envigado"),
    ("itagui", "Itagüí"),
    ("bello", "Bello"),
    ("rionegro", "Rionegro"),
]


async def scrape_computrabajo(max_pages=3):
    """Scrape Computrabajo with Playwright"""
    if not PLAYWRIGHT_AVAILABLE:
        logger.error("Playwright not installed")
        return []
    
    jobs = []
    
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled', '--no-sandbox']
        )
        
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            locale='es-CO',
        )
        
        page = await context.new_page()
        
        for location_slug, location_name in LOCATIONS:
            for page_num in range(1, max_pages + 1):
                try:
                    url = f"https://co.computrabajo.com/empleos-de-{location_slug}"
                    url = url + f"?p={page_num}" if page_num > 1 else url
                    
                    logger.info(f"Computrabajo: {location_name} page {page_num}")
                    
                    await page.goto(url, wait_until='networkidle', timeout=20000)
                    await asyncio.sleep(1.5)
                    
                    content = await page.content()
                    soup = BeautifulSoup(content, 'lxml')
                    
                    containers = soup.select("article.box_offer, div.box_offer")
                    logger.info(f"Found {len(containers)} jobs")
                    
                    for el in containers:
                        try:
                            title_el = el.select_one("a[href*='/oferta-de-trabajo'], h2 a")
                            title = title_el.get_text(strip=True) if title_el else ""
                            
                            company_el = el.select_one("a[class*='enterprise'], span.icon-li-icon")
                            company = company_el.get_text(strip=True) if company_el else "No especificada"
                            if not company or company == "N/A":
                                for span in el.select("span"):
                                    t = span.get_text(strip=True)
                                    if t and t != title and len(t) < 80:
                                        company = t
                                        break
                            
                            location_el = el.select_one("span[class*='location'], p[class*='city']")
                            location = location_el.get_text(strip=True) if location_el else f"{location_name}, Antioquia"
                            
                            salary_el = el.select_one("span[class*='salary']")
                            salary = salary_el.get_text(strip=True) if salary_el else ""
                            
                            href = title_el.get('href', '') if title_el else ''
                            job_url = href if href.startswith('http') else f"https://co.computrabajo.com{href}" if href else ""
                            
                            if title:
                                jobs.append(JobPosting(
                                    title=title,
                                    company=company,
                                    location=location,
                                    salary_raw=salary,
                                    url=job_url,
                                    source="Computrabajo",
                                    date_posted=None,
                                ))
                        except Exception as e:
                            logger.debug(f"Parse error: {e}")
                            
                except Exception as e:
                    logger.warning(f"Error on {location_name} page {page_num}: {e}")
        
        await browser.close()
    
    return jobs


def deduplicate_jobs(jobs):
    seen = set()
    unique = []
    for job in jobs:
        if job.url and job.url not in seen:
            seen.add(job.url)
            unique.append(job)
    return unique


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("Running Computrabajo scraper with Playwright...")
    jobs = asyncio.run(scrape_computrabajo(max_pages=2))
    jobs = deduplicate_jobs(jobs)
    
    print(f"\nTotal jobs after deduplication: {len(jobs)}")
    
    import json
    from datetime import datetime
    
    jobs_data = [job.to_dict() for job in jobs]
    filename = f"empleos_antioquia_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(jobs_data, f, ensure_ascii=False, indent=2)
    
    print(f"Saved to {filename}")
    
    # Summary
    sources = {}
    for job in jobs:
        sources[job.source] = sources.get(job.source, 0) + 1
    print(f"\nBy source: {sources}")
