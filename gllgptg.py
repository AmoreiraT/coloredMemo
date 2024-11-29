import logging
import json
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraping_historico_pitangui.log'),
        logging.StreamHandler()
    ]
)

class ImageScraper:
    def __init__(self):
        self.setup_chrome()
        self.create_download_folder()
        self.fotos = []
        
    def setup_chrome(self):
        chrome_options = Options()
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')  # Run in headless mode
        self.driver = webdriver.Chrome(options=chrome_options)
        logging.info("Chrome driver initialized")

    def create_download_folder(self):
        if not os.path.exists('fotos_historicas_pitangui'):
            os.makedirs('fotos_historicas_pitangui')

    def scroll_page(self):
        SCROLL_PAUSE_TIME = 2
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
    def extract_image_info(self, img_element):
        try:
            img_url = img_element.get_attribute('src')
            if not img_url or 'data:' in img_url:
                img_url = img_element.get_attribute('data-src')
                
            if not img_url:
                return None
                
            img_alt = img_element.get_attribute('alt') or 'No description'
            logging.info(f"Found image: {img_url}")
            
            return {
                'url_imagem': img_url,
                'descricao': img_alt
            }
            
        except Exception as e:
            logging.error(f"Error extracting image: {str(e)}")
            return None
            
    def download_image(self, url, filename):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.google.com/'
            }
            
            response = requests.get(url, headers=headers, stream=True, timeout=10)
            response.raise_for_status()
            
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            # Verify file was downloaded
            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                logging.info(f"Successfully downloaded: {filename}")
                return True
            else:
                logging.error(f"Download failed or empty file: {filename}")
                return False
                
        except Exception as e:
            logging.error(f"Error downloading {url}: {str(e)}")
            return False
            
    def scrape_images(self):
        query = "fotos antigas Pitangui Minas Gerais"
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbm=isch"
        
        try:
            self.driver.get(url)
            logging.info(f"Accessing URL: {url}")
            
            # Wait for images to load
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[jsname="r5xl4"]')))
            
            # Scroll to load more images
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Get all image containers
            image_containers = self.driver.find_elements(By.CSS_SELECTOR, 'div[jsname="r5xl4"]')
            logging.info(f"Found {len(image_containers)} image containers")
            
            for index, container in enumerate(image_containers):
                try:
                    # Get image URL directly from the container
                    img = container.find_element(By.TAG_NAME, 'img')
                    img_url = img.get_attribute('src')
                    
                    # Try to get higher resolution URL
                    if 'data:' in img_url:
                        img_url = img.get_attribute('data-src')
                    if not img_url:
                        continue
                        
                    # Sometimes the URL is in data-iurl attribute
                    if not img_url.startswith('http'):
                        img_url = img.get_attribute('data-iurl')
                    
                    if img_url and img_url.startswith('http'):
                        filename = f"fotos_historicas_pitangui/pitangui_{index:03d}.jpg"
                        if self.download_image(img_url, filename):
                            info = {
                                'url_imagem': img_url,
                                'arquivo_local': filename,
                                'descricao': img.get_attribute('alt') or 'No description'
                            }
                            self.fotos.append(info)
                            logging.info(f"Successfully downloaded image {index}")
                            
                except Exception as e:
                    logging.error(f"Error processing container {index}: {str(e)}")
                    continue
                    
            logging.info(f"Total images downloaded: {len(self.fotos)}")
            
        except Exception as e:
            logging.error(f"Error in scrape_images: {str(e)}")
            
    def save_metadata(self):
        try:
            with open('fotos_historicas_pitangui/metadata.json', 'w', encoding='utf-8') as f:
                json.dump({
                    'fotos': self.fotos,
                    'total': len(self.fotos)
                }, f, ensure_ascii=False, indent=2)
            logging.info(f"Saved metadata for {len(self.fotos)} images")
        except Exception as e:
            logging.error(f"Error saving metadata: {str(e)}")
            
    def close(self):
        self.driver.quit()
        
def main():
    scraper = ImageScraper()
    try:
        scraper.scrape_images()
        scraper.save_metadata()
    finally:
        scraper.close()

if __name__ == "__main__":
    main()