from fastapi import testclient
from server import app


def test_simple_generate():
    client = testclient.TestClient(app)
    response = client.post(
        '/generate', 
        json={
        "prompt": "hello",
        "model": "llama3.2"
        },
        headers={
            'x-api-key': 'secret'
        }
    )
    assert response.status_code == 200
    print(response.json())
    