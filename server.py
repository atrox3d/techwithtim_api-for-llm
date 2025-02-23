from fastapi import Body, FastAPI, Depends, HTTPException, Header
import ollama

import apikey

app = FastAPI()

FAKE_CREDITS = 5
FAKE_APIKEY_STATUS = apikey.get_apikey_status_from_env(FAKE_CREDITS)


def verify_apykey(x_api_key:str=Header(None)) -> dict:
    credits = FAKE_APIKEY_STATUS.get(x_api_key, 0)
    if credits <= 0:
        raise HTTPException(status_code=401, detail='Invalid API key or no credits')
    return x_api_key


@app.post('/generate')
def generate(
    prompt      :str = Body(embed=True),
    model       :str = Body(default='mistral', embed=True),
    x_api_key   :str = Depends(verify_apykey)
):
    '''
    json structure:
    {
        "prompt": "actual prompt",
        "model" : "llama3.2"        # OPTIONAL
    }
    '''
    FAKE_APIKEY_STATUS[x_api_key] -= 1
    
    response = ollama.chat(
            model=model,
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                },
            ]
    )
    return {
        'response': response.message.content,
        'credits': FAKE_APIKEY_STATUS[x_api_key]
        }

