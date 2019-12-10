import json
from . import api
from flask import request
from app.server.user_server import UserServer


# 登陆
@api.route('/login', methods=['POST'])
def api_login():
    result = {'result': 'OK', 'error': ''}
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    res, msg = UserServer().login(**json_data)
    if not res:
        result['result'] = 'NG'
        result['error'] = msg
    else:
        result['content'] = msg
    return result


# 注册
@api.route('/sign', methods=['POST'])
def api_sign():
    result = {'result': 'OK', 'error': ''}
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    res, msg = UserServer().sign(**json_data)
    if not res:
        result['result'] = 'NG'
        result['error'] = msg
    return result

# 删除用户
@api.route('/user', methods=['delete'])
def api_user():
    result = {'result': 'OK', 'error': ''}
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    user_id = json_data.get('user_id')
    res, msg = UserServer().del_user(user_id)
    if not res:
        result['result'] = 'NG'
        result['error'] = msg
    return result


# 用户列表
@api.route('/user/list/<int:user_id>', methods=['get'])
def api_user_list(user_id):
    result = {'result': 'OK', 'error': ''}
    res, msg = UserServer().get_user_list(user_id)
    if not res:
        result['result'] = 'NG'
        result['error'] = msg
    else:
        result['content'] = msg
    return result

# 设置角色
@api.route('/user/role', methods=['post'])
def api_user_role():
    result = {'result': 'OK', 'error': ''}
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    res, msg = UserServer().assign_user_role(**json_data)
    if not res:
        result['result'] = 'NG'
        result['error'] = msg
    return result

# 更新个人信息
@api.route('/user/update/<int:user_id>', methods=['post'])
def api_user_update(user_id):
    result = {'result': 'OK', 'error': ''}
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    res, msg = UserServer().update_user(user_id, **json_data)
    if not res:
        result['result'] = 'NG'
        result['error'] = msg
    return result
