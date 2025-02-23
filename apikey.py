import os
from dotenv import load_dotenv


load_dotenv()

def get_apikey(provider:str='env') -> str:
    '''
    TODO: implement other sources like db, ...
    '''
    if provider == 'env':
        return os.getenv('API_KEY')
    raise ValueError(f'expected provider={'env'!r}')


def get_apikey_credits(apikey:str, credits:int=10) -> dict:
    '''
    TODO: implement other sources like db, ...
    '''
    return {
        apikey: credits
    }


def get_apikey_status_from_env(credits:int=0) -> dict:
    '''
    good for the exampl
    '''
    apikey = get_apikey()
    return get_apikey_credits(apikey, credits)

