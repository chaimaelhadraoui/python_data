from flask import Blueprint, request, jsonify

from src.api.sqlalchemy_local import add_object
from src.constants import AGGREGATOR_MODEL_PATH
from src.models.aggregator_model import AggregatorModel
import numpy as np
from src.api.model import result_model

model = AggregatorModel()
model.load(AGGREGATOR_MODEL_PATH)
blueprint = Blueprint('api', __name__, url_prefix='/api')


@blueprint.route('/')
@blueprint.route('/index')
def index():
    return "CARD FRAUD DETECTION API - INFERENCE BLUEPRINT"


@blueprint.route('/inference', methods=['POST'])
def run_inference():
    if request.method == 'POST':
        features = np.array(request.json).reshape(1, -1)
        prediction = model.predict(features)
        return str(prediction[0])


@blueprint.route('/save', methods=['POST','GET'])
def save_result():
    if request.method == 'POST':
        result = request.json.get('result')

        a_result = result_model.Result(result=result)
        try:
            if add_object(a_result):
                return result + " added to database"
        except Exception as e:
            return jsonify({'error': e, 'code': 400})
    return jsonify({'error': 'Only post requests are supported', 'code': 400})
