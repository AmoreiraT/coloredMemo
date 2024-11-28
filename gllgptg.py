import logging
import json
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Configuração do logging
logging.basicConfig(filename='scraping_google_imagens.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# URL de busca no Google Imagens
search_url = "https://www.google.com/search?q=acervos+hist%C3%B3ricos+de+Pitangui&tbm=isch"

# Criar pasta para downloads
if not os.path.exists('fotos_acervos_pitangui'):
    os.makedirs('fotos_acervos_pitangui')
    logging.info("Pasta 'fotos_acervos_pitangui' criada.")

def extrair_informacoes(driver):
    """Extrai informações das imagens do Google Imagens."""
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        imagens = []

        # Selecionar blocos de imagem
        for img_div in soup.select('div[jsname="N9Xkfe"]'):
            try:
                # URL da imagem
                url_imagem = img_div.select_one('img')['src']
                
                # Referência da imagem
                referencia = img_div.select_one('a[jsname="hSRGPd"]').text.strip()
                url_referencia = img_div.select_one('a[jsname="hSRGPd"]')['href']
                url_referencia = f"https://www.google.com{url_referencia}"

                # Créditos
                creditos = img_div.select_one('span[jsname="sTFXNd"]').text.strip()

                # Verificar se a imagem é de Pitangui antiga
                descricao = img_div.select_one('img')['alt']
                if any(keyword in descricao.lower() for keyword in ["pitangui", "1950", "preto e branco", "histórica"]):
                    imagens.append({
                        'url_imagem': url_imagem,
                        'referencia': referencia,
                        'url_referencia': url_referencia,
                        'creditos': creditos,
                        'descricao': descricao
                    })
                    logging.info(f"Informações da imagem extraídas: {url_imagem}")
                else:
                    logging.info(f"Imagem ignorada: {url_imagem} - Descrição: {descricao}")

            except Exception as e:
                logging.error(f"Erro ao extrair informações da imagem: {e}")
                continue

        return imagens
    except Exception as e:
        logging.error(f"Erro ao extrair informações: {e}")
        return []

def baixar_imagem(url_imagem, nome_arquivo):
    """Baixa a imagem da URL fornecida."""
    try:
        response = requests.get(url_imagem, stream=True)
        response.raise_for_status()
        with open(nome_arquivo, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        logging.info(f"Imagem baixada: {nome_arquivo}")
    except Exception as e:
        logging.error(f"Erro ao baixar imagem: {e}")

def extrair_detalhes_imagem(url_referencia):
    """Extrai detalhes adicionais da página de referência da imagem."""
    try:
        response = requests.get(url_referencia)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extraímos informações adicionais, como textos relevantes que possam estar na página
        detalhes = soup.get_text(separator=' ', strip=True)
        return detalhes
    except Exception as e:
        logging.error(f"Erro ao extrair detalhes da referência: {e}")
        return ""

# Inicializar o driver do Chrome
driver = webdriver.Chrome()

# Lista para armazenar os dados das fotos
fotos = []

try:
    # Acessar a página de busca do Google Imagens
    driver.get(search_url)

    # Aguardar o carregamento dos resultados (ajuste o tempo de espera se necessário)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[jsname="N9Xkfe"]'))
    )

    # Extrair informações das imagens
    imagens = extrair_informacoes(driver)

    for img_info in imagens:
        nome_imagem = f"fotos_acervos_pitangui/{img_info['url_imagem'].split('/')[-1]}"
        baixar_imagem(img_info['url_imagem'], nome_imagem)
        img_info['nome_arquivo'] = nome_imagem
        
        # Extrair detalhes adicionais da página de referência
        detalhes = extrair_detalhes_imagem(img_info['url_referencia'])
        img_info['detalhes'] = detalhes
        
        fotos.append(img_info)
    
except Exception as e:
    logging.error(f"Erro ao processar página: {e}")

finally:
    # Fechar o navegador
    driver.quit()

# Salvar os dados em um arquivo JSON
with open('fotos_acervos_pitangui/metadata.json', 'w', encoding='utf-8') as f:
    json.dump(fotos, f, ensure_ascii=False, indent=4)

logging.info(f"Processo concluído. {len(fotos)} fotos encontradas e salvas.")