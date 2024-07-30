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
    
    