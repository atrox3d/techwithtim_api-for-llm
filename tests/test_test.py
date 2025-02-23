from fastapi import HTTPException, testclient
import os
import pytest

from server import app, FAKE_APIKEY_STATUS, FAKE_CREDITS


@pytest.fixture
def apikey_status() -> dict:
    return FAKE_APIKEY_STATUS


@pytest.fixture
def apikey(apikey_status) -> str:
    key, = apikey_status.keys()
    return key


@pytest.fixture
def apikey_credits(apikey, apikey_status) -> int:
    return apikey_status[apikey]


def test_simple_generate_with_model(apikey):
    client = testclient.TestClient(app)
    
    response = client.post(
            '/generate', 
            json={
                "prompt": "hello",
                "model": "llama3.2"
            },
            headers={
                'x-api-key': apikey
            }
    )
    assert response.status_code == 200
    assert 'hello' in response.text.lower()
    print(response.json())


def test_simple_generate_default_model(apikey):
    client = testclient.TestClient(app)
    
    response = client.post(
            '/generate', 
            json={
                "prompt": "hello",
            },
            headers={
                'x-api-key': apikey
            }
    )
    assert response.status_code == 200
    assert 'hello' in response.text.lower()
    print(response.json())


def test_credits(apikey, apikey_credits):
    client = testclient.TestClient(app)
    
    for _ in range(apikey_credits):
        response = client.post(
                '/generate', 
                json={
                    "prompt": "hello",
                },
                headers={
                    'x-api-key': apikey
                }
        )
    assert response.json()['credits'] == 0


def test_invalid_credits(apikey, apikey_credits):
    client = testclient.TestClient(app)
    
    for _ in range(apikey_credits +1):
        response = client.post(
                '/generate', 
                json={
                    "prompt": "hello",
                },
                headers={
                    'x-api-key': apikey
                }
        )
    print(response.json())
    assert response.status_code == 401
    assert response.json() == {'detail': 'Invalid API key or no credits'}
