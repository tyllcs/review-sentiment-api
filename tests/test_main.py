from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch


client = TestClient(app)

def test_predict():
    review = "I can't eat this. It's bad!"
    response = client.post('/predict', json={'text': review})
    assert response.status_code == 200
    assert 'sentiment' in response.json()
    assert response.json()['sentiment'] in ['positive', 'negative']

def test_predict_empty_string():
    response = client.post('/predict', json={'text': ""})
    assert response.status_code == 422

def test_predict_string_of_spaces():
    response = client.post('/predict', json={'text': "     "})
    assert response.status_code == 422

def test_predict_int_type():
    response = client.post('/predict', json={'text': 123})
    assert response.status_code == 422

def test_predict_cyrillic_symbols():
    response = client.post('/predict', json={'text': "привет"})
    assert response.status_code == 422

def test_predict_without_text_field():
    response = client.post('/predict', json={})
    assert response.status_code == 422

def test_predict_sentiment():
    with patch("main.predict_sentiment", return_value="negative") as input_mock:
        response = client.post('/predict', json={'text': 'Bad'})
    assert response.json()['sentiment'] == 'negative'
    input_mock.assert_called_once()
    assert input_mock.call_args.args[0] == "Bad"
