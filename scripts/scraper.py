"""
Web Scraper para Books to Scrape
Extrai informações de livros do site https://books.toscrape.com/
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
from typing import List, Dict, Optional
from pathlib import Path
import re

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BooksScraper:
    """Classe para realizar web scraping de livros"""
    
    BASE_URL = "https://books.toscrape.com"
    RATING_MAP = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }
    
    def __init__(self, base_url: str = None):
        """
        Inicializa o scraper
        
        Args:
            base_url: URL base do site (opcional)
        """
        self.base_url = base_url or self.BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def _extract_rating(self, book_element) -> int:
        """Extrai o rating do livro"""
        star_rating = book_element.find('p', class_='star-rating')
        if star_rating:
            rating_class = star_rating.get('class', [])
            for cls in rating_class:
                if cls in self.RATING_MAP:
                    return self.RATING_MAP[cls]
        return 0
    
    def _extract_price(self, price_text: str) -> float:
        """Extrai o valor numérico do preço"""
        try:
            # Remove símbolos de moeda e converte para float
            price_clean = re.sub(r'[^\d.]', '', price_text)
            return float(price_clean)
        except (ValueError, AttributeError):
            return 0.0
    
    def _extract_availability(self, availability_text: str) -> Dict[str, any]:
        """Extrai informações de disponibilidade"""
        if not availability_text:
            return {'in_stock': False, 'quantity': 0}
        
        in_stock = 'in stock' in availability_text.lower()
        
        # Tenta extrair quantidade
        quantity_match = re.search(r'\((\d+) available\)', availability_text)
        quantity = int(quantity_match.group(1)) if quantity_match else (1 if in_stock else 0)
        
        return {
            'in_stock': in_stock,
            'quantity': quantity
        }
    
    def scrape_book_details(self, book_url: str) -> Dict[str, any]:
        """
        Extrai detalhes completos de um livro individual
        
        Args:
            book_url: URL da página do livro
            
        Returns:
            Dicionário com informações detalhadas do livro
        """
        try:
            response = self.session.get(book_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Informações da tabela de produto
            product_info = {}
            table = soup.find('table', class_='table-striped')
            if table:
                for row in table.find_all('tr'):
                    th = row.find('th')
                    td = row.find('td')
                    if th and td:
                        product_info[th.text.strip()] = td.text.strip()
            
            # Descrição
            description_tag = soup.find('div', id='product_description')
            description = ''
            if description_tag:
                description_p = description_tag.find_next_sibling('p')
                if description_p:
                    description = description_p.text.strip()
            
            return {
                'upc': product_info.get('UPC', ''),
                'product_type': product_info.get('Product Type', ''),
                'price_excl_tax': product_info.get('Price (excl. tax)', ''),
                'price_incl_tax': product_info.get('Price (incl. tax)', ''),
                'tax': product_info.get('Tax', ''),
                'number_of_reviews': int(product_info.get('Number of reviews', 0)),
                'description': description
            }
        except Exception as e:
            logger.error(f"Erro ao extrair detalhes do livro {book_url}: {e}")
            return {}
    
    def scrape_page(self, page_url: str) -> List[Dict[str, any]]:
        """
        Extrai informações de todos os livros de uma página
        
        Args:
            page_url: URL da página a ser extraída
            
        Returns:
            Lista de dicionários com informações dos livros
        """
        books = []
        
        try:
            logger.info(f"Extraindo página: {page_url}")
            response = self.session.get(page_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            book_elements = soup.find_all('article', class_='product_pod')
            
            for idx, book in enumerate(book_elements, 1):
                try:
                    # Título e URL
                    title_tag = book.find('h3').find('a')
                    title = title_tag.get('title', '')
                    book_relative_url = title_tag.get('href', '')
                    book_url = f"{self.base_url}/catalogue/{book_relative_url.replace('../', '')}"
                    
                    # Preço
                    price_tag = book.find('p', class_='price_color')
                    price_text = price_tag.text if price_tag else '£0.00'
                    price = self._extract_price(price_text)
                    
                    # Rating
                    rating = self._extract_rating(book)
                    
                    # Disponibilidade
                    availability_tag = book.find('p', class_='instock availability')
                    availability_text = availability_tag.text.strip() if availability_tag else ''
                    availability = self._extract_availability(availability_text)
                    
                    # Imagem
                    img_tag = book.find('img')
                    image_url = ''
                    if img_tag:
                        img_relative = img_tag.get('src', '')
                        image_url = f"{self.base_url}/{img_relative.replace('../', '')}"
                    
                    # Categoria (pegamos da breadcrumb na página de detalhes)
                    # Por enquanto vamos deixar vazio e preencher depois
                    category = ''
                    
                    book_data = {
                        'title': title,
                        'price': price,
                        'price_text': price_text,
                        'rating': rating,
                        'in_stock': availability['in_stock'],
                        'quantity': availability['quantity'],
                        'availability_text': availability_text,
                        'image_url': image_url,
                        'book_url': book_url,
                        'category': category
                    }
                    
                    books.append(book_data)
                    logger.debug(f"Livro extraído: {title}")
                    
                except Exception as e:
                    logger.error(f"Erro ao extrair livro {idx}: {e}")
                    continue
            
            logger.info(f"Total de livros extraídos da página: {len(books)}")
            
        except Exception as e:
            logger.error(f"Erro ao processar página {page_url}: {e}")
        
        return books
    
    def scrape_category(self, category_url: str, category_name: str) -> List[Dict[str, any]]:
        """
        Extrai todos os livros de uma categoria específica
        
        Args:
            category_url: URL da categoria
            category_name: Nome da categoria
            
        Returns:
            Lista de dicionários com informações dos livros
        """
        all_books = []
        current_url = category_url
        page_num = 1
        
        while current_url:
            logger.info(f"Extraindo categoria '{category_name}' - Página {page_num}")
            
            try:
                response = self.session.get(current_url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'lxml')
                
                # Extrair livros da página
                books = self.scrape_page(current_url)
                
                # Adicionar categoria aos livros
                for book in books:
                    book['category'] = category_name
                
                all_books.extend(books)
                
                # Verificar se há próxima página
                next_button = soup.find('li', class_='next')
                if next_button:
                    next_link = next_button.find('a')
                    if next_link:
                        next_relative_url = next_link.get('href', '')
                        # Construir URL completa da próxima página
                        base_category_url = current_url.rsplit('/', 1)[0]
                        current_url = f"{base_category_url}/{next_relative_url}"
                        page_num += 1
                        time.sleep(0.5)  # Pausa educada entre requisições
                    else:
                        current_url = None
                else:
                    current_url = None
                    
            except Exception as e:
                logger.error(f"Erro ao processar categoria '{category_name}': {e}")
                break
        
        logger.info(f"Total de livros na categoria '{category_name}': {len(all_books)}")
        return all_books
    
    def get_all_categories(self) -> List[Dict[str, str]]:
        """
        Obtém lista de todas as categorias disponíveis
        
        Returns:
            Lista de dicionários com nome e URL de cada categoria
        """
        categories = []
        
        try:
            logger.info("Obtendo lista de categorias...")
            response = self.session.get(f"{self.base_url}/index.html", timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            category_list = soup.find('ul', class_='nav-list')
            
            if category_list:
                # Pega todas as categorias exceto a primeira (que é "Books")
                category_links = category_list.find('ul').find_all('a')
                
                for link in category_links:
                    category_name = link.text.strip()
                    category_relative_url = link.get('href', '')
                    category_url = f"{self.base_url}/{category_relative_url}"
                    
                    categories.append({
                        'name': category_name,
                        'url': category_url
                    })
            
            logger.info(f"Total de categorias encontradas: {len(categories)}")
            
        except Exception as e:
            logger.error(f"Erro ao obter categorias: {e}")
        
        return categories
    
    def scrape_all_books(self) -> pd.DataFrame:
        """
        Extrai todos os livros de todas as categorias do site
        
        Returns:
            DataFrame pandas com todos os livros
        """
        logger.info("Iniciando scraping completo do site...")
        
        all_books = []
        categories = self.get_all_categories()
        
        for idx, category in enumerate(categories, 1):
            logger.info(f"\n{'='*60}")
            logger.info(f"Categoria {idx}/{len(categories)}: {category['name']}")
            logger.info(f"{'='*60}")
            
            books = self.scrape_category(category['url'], category['name'])
            all_books.extend(books)
            
            # Pausa entre categorias
            time.sleep(1)
        
        # Criar DataFrame
        df = pd.DataFrame(all_books)
        
        # Adicionar ID único
        if not df.empty:
            df.insert(0, 'id', range(1, len(df) + 1))
        
        logger.info(f"\n{'='*60}")
        logger.info(f"SCRAPING COMPLETO!")
        logger.info(f"Total de livros extraídos: {len(df)}")
        logger.info(f"Total de categorias: {len(categories)}")
        logger.info(f"{'='*60}\n")
        
        return df
    
    def save_to_csv(self, df: pd.DataFrame, filepath: str):
        """
        Salva DataFrame em arquivo CSV
        
        Args:
            df: DataFrame a ser salvo
            filepath: Caminho do arquivo CSV
        """
        try:
            # Criar diretório se não existir
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            # Salvar CSV
            df.to_csv(filepath, index=False, encoding='utf-8')
            logger.info(f"Dados salvos com sucesso em: {filepath}")
            
            # Exibir estatísticas
            logger.info(f"\nEstatísticas dos dados:")
            logger.info(f"- Total de registros: {len(df)}")
            logger.info(f"- Colunas: {', '.join(df.columns.tolist())}")
            logger.info(f"- Categorias únicas: {df['category'].nunique()}")
            logger.info(f"- Preço médio: £{df['price'].mean():.2f}")
            logger.info(f"- Rating médio: {df['rating'].mean():.2f}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar arquivo CSV: {e}")
            raise


def main():
    """Função principal para executar o scraping"""
    scraper = BooksScraper()
    
    # Realizar scraping
    df_books = scraper.scrape_all_books()
    
    # Salvar em CSV
    scraper.save_to_csv(df_books, 'data/books.csv')
    
    print("\n✅ Scraping concluído com sucesso!")
    print(f"📊 Arquivo salvo em: data/books.csv")
    print(f"📚 Total de livros: {len(df_books)}")


if __name__ == "__main__":
    main()



