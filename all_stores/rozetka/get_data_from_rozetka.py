import aiohttp
from bs4 import BeautifulSoup 


async def get_product_data_from_rozetka(url):
    '''Парсить і отримує інфромацію про товар'''

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    }
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url) as response:
                    html = await response.text()  # Отримуємо текст відповіді
    except:
        return None
                
    soup = BeautifulSoup(html, "html.parser")  # Використовуємо html.parser

    try:
        name = soup.find('h1', class_='h2 bold ng-star-inserted').text.strip()
    except:
        name = None
    
    try: 
        price = float(''.join((soup.find('p', class_='product-price__big').text.strip()[:-1]).split()))
    except:
        price = None
        
    try: 
        state = soup.find('p', class_='status-label status-label--gray ng-star-inserted').text.strip()
    except:
        try:
            state = soup.find('p', class_='status-label status-label--orange ng-star-inserted').text.strip()
        except:
            try:
                state = soup.find('p', class_='status-label status-label--green ng-star-inserted').text.strip()
            except:
                state = None
        
    try: 
        max_price = float(''.join((soup.find('p', class_='product-price__small ng-star-inserted').text.strip()[:-1]).split()))
    except:
        max_price = None
        
    try:
        currency = soup.find('p', class_='product-price__big').text.strip()[-1]
    except:
        currency = None
        
    return name, price, max_price, currency, state