from fastapi import Body, FastAPI
import ollama

app = FastAPI()

@app.post('/generate')
def generate(
    prompt:str = Body(embed=True)   # {"prompt": "actual prompt"}
                                    # without using pydantic model
):
    print(f'{prompt = }')
    response = ollama.chat(
            model='mistral',
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                },
            ]
    )
    return {'response': response.message.content}

