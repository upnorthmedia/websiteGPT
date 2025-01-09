import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo, showerror

class SitemapScraper:
    def __init__(self, output_folder='output'):
        self.output_folder = output_folder
        self.scraped_content = {}  # Add this to store content
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-images')  # Disable images
        self.driver = webdriver.Chrome(options=chrome_options)

    def fetch_sitemap(self, sitemap_url):
        """Fetch and parse sitemap XML."""
        try:
            response = requests.get(sitemap_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'xml')
            urls = [loc.text for loc in soup.find_all('loc')]
            return urls
        except requests.RequestException as e:
            showerror("Error", f"Error fetching sitemap: {e}")
            return []

    def sanitize_filename(self, url):
        """Convert URL to a valid filename."""
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        if not path:
            path = 'index'
        return f"{path.replace('/', '_')}.pdf"

    def save_as_text(self, url):
        """Save webpage content as text after rendering JavaScript."""
        try:
            filename = self.sanitize_filename(url).replace('.pdf', '.txt')
            
            print(f"Fetching {url}...")
            self.driver.get(url)
            
            # Wait for the page to load (adjust timeout as needed)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Get the rendered text
            text_content = self.driver.find_element(By.TAG_NAME, "body").text
            
            # Store content in dictionary instead of saving directly
            self.scraped_content[filename] = text_content
            
            showinfo("Info", f"Processed {filename}")
            return True
        except Exception as e:
            showerror("Error", f"Error saving text for {url}: {e}")
            return False

    def process_sitemap(self, sitemap_url):
        """Process entire sitemap and save all pages as text."""
        urls = self.fetch_sitemap(sitemap_url)
        if not urls:
            showerror("Error", "No URLs found in sitemap.")
            return {}

        showinfo("Info", f"Found {len(urls)} URLs in sitemap.")
        try:
            for url in urls:
                self.save_as_text(url)
                time.sleep(1)
        finally:
            self.driver.quit()  # Ensure browser is closed
        
        return self.scraped_content  # Return the collected content

def get_user_preference():
    while True:
        choice = askstring("File Input",
"""
Choose output format:
1. Individual files (one file per page)
2. Single merged file (all pages in one file with headers)

Enter 1 or 2: """).strip()
        
        if choice in ['1', '2']:
            return choice == '2'  # Returns True for merged, False for individual
        print("Invalid choice. Please enter 1 or 2.")

def main():
    # Get user preference at start
    merge_files = get_user_preference()
    
    sitemap_url = askstring("Url Input", "Enter sitemap URL (e.g., https://example.com/sitemap.xml): ")
    scraper = SitemapScraper()
    scraped_content = scraper.process_sitemap(sitemap_url)  # Get the content

    # Handle output based on user preference
    if merge_files and scraped_content:
        # Merged file output
        with open('merged_output.txt', 'w', encoding='utf-8') as f:
            for filename, content in scraped_content.items():
                f.write(f"\n{'='*50}\n")
                f.write(f"{filename}\n")
                f.write(f"{'='*50}\n\n")
                f.write(content)
                f.write('\n\n')
    elif scraped_content:
        # Individual files output
        for filename, content in scraped_content.items():
            with open(f"output/{filename}", 'w', encoding='utf-8') as f:
                f.write(content)
    else:
        showerror("Error", "No Content to save")

if __name__ == "__main__":
    main()
