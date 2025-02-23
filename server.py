from fastapi import Body, FastAPI, Depends, HTTPException, Header
import ollama

import apikey

app = FastAPI()

@app.post('/generate')
def generate(
    prompt:str = Body(embed=True)   
    ,model:str = Body(default='mistral', embed=True)
):
    '''
    json structure:
    {
        "prompt": "actual prompt",
        "model" : "llama3.2"        # OPTIONAL
    }
    '''
    print(f'{prompt = }')
    print(f'{model = }')
    response = ollama.chat(
            model=model,
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                },
            ]
    )
    return {'response': response.message.content}

