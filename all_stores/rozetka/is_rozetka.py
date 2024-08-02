import aiohttp
from bs4 import BeautifulSoup 


async def is_rozetka(url: str):
    '''Перевіряє чи силка веде саме на сайт розетки'''
    try:
        url = url.split('//')
        url = url[1].split('/')
        url = url[0].split('.')
        
        for el in url:
            if el == 'rozetka':
                return True
        
        return False
    except:
        return False
    



async def is_product_rozetka(url):
    '''Перевіряє чи силка веде саме на сторінку з товаром'''
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    }
    
    async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                html = await response.text() 
                
            soup = BeautifulSoup(html, "html.parser")

            element = soup.find('h1', class_='h2 bold ng-star-inserted')
            if element:
                return True
            else:
                return False