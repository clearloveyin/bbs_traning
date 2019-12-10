import json
from . import api
from flask import request
from app.server.model_server import ModelServer


@api.route('/model', methods=['POST', 'GET'])
def api_model():
    result = {'result': 'OK', 'error': ''}
    if request.method == 'GET':
        model_list = ModelServer().get_models()
        result['content'] = model_list
    elif request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode("utf-8"))
        res, msg = ModelServer().add_model(**json_data)
        if not res:
            result['result'] = 'NG'
            result['error'] = msg
    return result


@api.route('/model/del', methods=['DELETE'])
def api_model_del():
    result = {'result': 'OK', 'error': ''}
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    model_id = json_data.get('model_id')
    user_id = json_data.get('user_id')
    res, msg = ModelServer().delete_model_by_id(model_id, user_id)
    if not res:
        result['result'] = 'NG'
        result['error'] = msg
    return result
