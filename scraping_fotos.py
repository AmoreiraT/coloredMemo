import logging
import json
import os
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Configuração do logging
logging.basicConfig(filename='scraping_pitangui.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# URL da busca avançada
search_url = "http://www.siaapm.cultura.mg.gov.br/modules/fotografico_docs/search.php?query=pitangui&andor=AND&tipo=0&fundo_colecoes=0&local=0&dta_ini=&dta_fim=&ordenar=0&asc_desc=10&action=results"

# Criar pasta para downloads
if not os.path.exists('fotos_pitangui'):
    os.makedirs('fotos_pitangui')
    logging.info("Pasta 'fotos_pitangui' criada.")

def extrair_informacoes(driver):
    """Extrai informações da página da foto."""
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Ajustar seletores CSS conforme necessário
        titulo = soup.select_one('h2.titulo').text.strip() if soup.select_one('h2.titulo') else ""
        descricao = soup.select_one('.descricao').text.strip() if soup.select_one('.descricao') else ""
        referencias = soup.select_one('.referencias').text.strip() if soup.select_one('.referencias') else ""
        notacao = soup.select_one('.notacao').text.strip() if soup.select_one('.notacao') else ""
        autor = soup.select_one('.autor').text.strip() if soup.select_one('.autor') else ""
        local = soup.select_one('.local').text.strip() if soup.select_one('.local') else ""
        data = soup.select_one('.data').text.strip() if soup.select_one('.data') else ""
        cor = soup.select_one('.cor').text.strip() if soup.select_one('.cor') else ""
        dimensao = soup.select_one('.dimensao').text.strip() if soup.select_one('.dimensao') else ""
        notas = soup.select_one('.notas').text.strip() if soup.select_one('.notas') else ""
        descritores = soup.select_one('.descritores').text.strip() if soup.select_one('.descritores') else ""
        
        # Encontrar a URL da imagem (considerando que pode estar em tags diferentes)
        imagem = soup.find('img', src=lambda src: src and 'fotografico' in src)
        if imagem:
            url_imagem = urljoin(driver.current_url, imagem['src'])
            logging.info(f"URL da imagem encontrada: {url_imagem}")
        else:
            url_imagem = None
            logging.warning("URL da imagem não encontrada.")

        # Log dos dados extraídos para depuração
        logging.info(f"Título: {titulo}, Descrição: {descricao}, Referências: {referencias}, Notação: {notacao}, "
                     f"Autor: {autor}, Local: {local}, Data: {data}, Cor: {cor}, Dimensão: {dimensao}, "
                     f"Notas: {notas}, Descritores: {descritores}")

        return {
            'titulo': titulo,
            'descricao': descricao,
            'referencias': referencias,
            'notacao': notacao,
            'autor': autor,
            'local': local,
            'data': data,
            'cor': cor,
            'dimensao': dimensao,
            'notas': notas,
            'descritores': descritores,
            'url_imagem': url_imagem,
        }
    except Exception as e:
        logging.error(f"Erro ao extrair informações: {e}")
        return None

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

def navegar_paginas(driver):
    """Navega por todas as páginas de resultados e extrai informações das fotos."""
    while True:
        # Extrair links das fotos na página atual
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        links_fotos = soup.select('a[href*="photo.php?lid="]')

        for link in links_fotos:
            foto_url = urljoin(driver.current_url, link['href'])
            # Abrir nova aba e acessar o link da foto
            driver.execute_script("window.open(arguments[0]);", foto_url)

            # Mudar para a nova aba
            driver.switch_to.window(driver.window_handles[1])

            # Aguardar o carregamento da imagem
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'img[src*="fotografico"]'))
                )
            except TimeoutException:
                logging.error(f"Tempo limite excedido para carregar a imagem na página: {driver.current_url}")
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                continue

            # Extrair informações e baixar a imagem
            informacoes = extrair_informacoes(driver)
            if informacoes and informacoes['url_imagem']:
                nome_imagem = f"fotos_pitangui/{informacoes['url_imagem'].split('/')[-1]}"
                baixar_imagem(informacoes['url_imagem'], nome_imagem)
                informacoes['nome_arquivo'] = nome_imagem
                fotos.append(informacoes)

            # Fechar a aba da foto
            driver.close()

            # Voltar para a aba principal
            driver.switch_to.window(driver.window_handles[0])

        # Verificar se há um link para a próxima página
        next_page = soup.select_one('a[href*="search.php?query=pitangui&"][title="Próxima"]')
        if next_page:
            next_page_url = urljoin(driver.current_url, next_page['href'])
            driver.get(next_page_url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="photo.php?lid="]'))
            )
        else:
            break

# Inicializar o driver do Chrome
driver = webdriver.Chrome()

# Lista para armazenar os dados das fotos
fotos = []

try:
    # Acessar a página de resultados da busca avançada
    driver.get(search_url)

    # Aguardar o carregamento dos resultados (ajuste o tempo de espera se necessário)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="photo.php?lid="]'))
    )

    # Navegar por todas as páginas de resultados
    navegar_paginas(driver)

except Exception as e:
    logging.error(f"Erro ao processar página: {e}")

finally:
    # Fechar o navegador
    driver.quit()

# Salvar os dados em um arquivo JSON
with open('fotos_pitangui/metadata.json', 'w', encoding='utf-8') as f:
    json.dump(fotos, f, ensure_ascii=False, indent=4)

logging.info(f"Processo concluído. {len(fotos)} fotos encontradas e salvas.")