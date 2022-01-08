import requests

from src.constants import INFERENCE_EXAMPLE


def test_index():
    result = requests.get(
        'http://localhost:5000/api/'
    )
    assert result.text == "CARD FRAUD DETECTION API - INFERENCE BLUEPRINT"


def test_run_inference():
    result = requests.post(
        'http://localhost:5000/api/inference',
        json=INFERENCE_EXAMPLE
    )
    assert int(result.text) == 1 or int(result.text) == 1 == 0


def test_save_result():
    result = requests.post(
        'http://localhost:5000/api/save',
        json={'result': 'Transaction: Fraudulent'}
    )
    assert result.text == 'Transaction: Fraudulent added to database'
