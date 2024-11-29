import logging
import json
import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options

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
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8'
            }
            
            response = requests.get(url, headers=headers, stream=True, timeout=10)
            response.raise_for_status()
            
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            logging.info(f"Downloaded: {filename}")
            return True
            
        except Exception as e:
            logging.error(f"Error downloading {url}: {str(e)}")
            return False
            
    def scrape_images(self):
        query = "fotos antigas Pitangui Minas Gerais"
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbm=isch"
        
        try:
            self.driver.get(url)
            time.sleep(3)  # Wait for images to load
            
            # Find all image elements
            images = self.driver.find_elements(By.CSS_SELECTOR, 'img.rg_i')
            logging.info(f"Found {len(images)} images")
            
            for index, img in enumerate(images):
                try:
                    info = self.extract_image_info(img)
                    if info and info['url_imagem']:
                        filename = f"fotos_historicas_pitangui/pitangui_{index:03d}.jpg"
                        if self.download_image(info['url_imagem'], filename):
                            info['arquivo_local'] = filename
                            self.fotos.append(info)
                            
                except Exception as e:
                    logging.error(f"Error processing image {index}: {str(e)}")
                    continue
                    
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