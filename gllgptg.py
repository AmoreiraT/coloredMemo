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
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

# Configure logging
logging.basicConfig(filename='scraping_historico_pitangui.log', level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

class ImageScraper:
    def __init__(self):
        self.setup_chrome()
        self.create_download_folder()
        self.fotos = []
        
    def setup_chrome(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        self.driver = webdriver.Chrome(options=chrome_options)
        
    def create_download_folder(self):
        if not os.path.exists('fotos_historicas_pitangui'):
            os.makedirs('fotos_historicas_pitangui')
            logging.info("Pasta 'fotos_historicas_pitangui' criada")
            
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
                
            img_alt = img_element.get_attribute('alt')
            
            # Click image to get more details
            img_element.click()
            time.sleep(1)
            
            # Get larger image
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'img.r48jcc'))
            )
            
            large_img = self.driver.find_element(By.CSS_SELECTOR, 'img.r48jcc')
            large_img_url = large_img.get_attribute('src')
            
            # Get source website
            source_element = self.driver.find_element(By.CSS_SELECTOR, 'div.K2DeBd a')
            source_url = source_element.get_attribute('href')
            source_text = source_element.text
            
            return {
                'url_imagem': large_img_url,
                'url_miniatura': img_url,
                'descricao': img_alt,
                'fonte': source_text,
                'url_fonte': source_url
            }
            
        except Exception as e:
            logging.error(f"Erro ao extrair informações da imagem: {str(e)}")
            return None
            
    def download_image(self, url, filename):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            return True
        except Exception as e:
            logging.error(f"Erro ao baixar imagem {url}: {str(e)}")
            return False
            
    def scrape_images(self):
        search_queries = [
            "fotos antigas Pitangui Minas Gerais",
            "Pitangui MG história fotografias",
            "Pitangui século XX fotos",
            "imagens históricas Pitangui"
        ]
        
        for query in search_queries:
            try:
                url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbm=isch"
                self.driver.get(url)
                
                self.scroll_page()
                
                images = self.driver.find_elements(By.CSS_SELECTOR, 'img.rg_i')
                
                for img in images:
                    info = self.extract_image_info(img)
                    if info:
                        filename = f"fotos_historicas_pitangui/{len(self.fotos):03d}.jpg"
                        if self.download_image(info['url_imagem'], filename):
                            info['arquivo_local'] = filename
                            self.fotos.append(info)
                            
            except Exception as e:
                logging.error(f"Erro ao processar busca '{query}': {str(e)}")
                
    def save_metadata(self):
        with open('fotos_historicas_pitangui/metadata.json', 'w', encoding='utf-8') as f:
            json.dump({
                'fotos': self.fotos,
                'total': len(self.fotos)
            }, f, ensure_ascii=False, indent=2)
            
    def close(self):
        self.driver.quit()
        
def main():
    scraper = ImageScraper()
    try:
        scraper.scrape_images()
        scraper.save_metadata()
        logging.info(f"Processo concluído. {len(scraper.fotos)} fotos encontradas e salvas.")
    finally:
        scraper.close()
        
if __name__ == "__main__":
    main()