import json
from . import api
from flask import request
from app.server.note_server import NoteServer


@api.route('/note/list/<list_type>', methods=['get'])
def api_latest_notes(list_type):
    result = {'result': 'OK', 'error': ''}
    note_list = []
    note_server = NoteServer()
    if list_type == 'newNote':
        # 最新帖子
        note_list = note_server.get_latest_notes()
    elif list_type == 'topNote':
        # 精华贴子
        note_list = note_server.get_notes_order_by_top()
    elif list_type == 'likeNote':
        # 点赞最多
        note_list = note_server.get_notes_order_by_like()
    elif list_type == 'issueNote':
        # 评论最多
        note_list = note_server.get_notes_order_by_issue()
    result['content'] = note_list
    return result


@api.route('/note/post', methods=['post'])
def api_post_notes():
    result = {'result': 'OK', 'error': ''}
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    res, msg = NoteServer().post_note(json_data)
    if not res:
        result['result'] = 'NG'
        result['error'] = msg
    return result


@api.route('/note/list/<int:model_id>', methods=['get'])
def api_note_list(model_id):
    result = {'result': 'OK', 'content': ''}
    note_list = NoteServer().get_notes_by_model_id(model_id)
    result['content'] = note_list
    return result


@api.route('/note/info/<int:note_id>', methods=['get'])
def api_note_info(note_id):
    result = {'result': 'OK', 'error': ''}
    res, msg = NoteServer().get_note_info(note_id)
    if not res:
        result['result'] = 'NG'
        result['error'] = msg
    else:
        result['content'] = msg
    return result


@api.route('/note/put', methods=['post', 'delete'])
def api_note_put():
    result = {'result': 'OK', 'error': ''}
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    if request.method == 'POST':
        res, msg = NoteServer().top_note(**json_data)
    elif request.method == 'DELETE':
        res, msg = NoteServer().del_note(**json_data)
    if not res:
        result['result'] = 'NG'
        result['error'] = msg
    else:
        result['content'] = msg
    return result


@api.route('/issue/note', methods=['post'])
def api_issue_note():
    result = {'result': 'OK', 'error': ''}
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    res, msg = NoteServer().issue_note(**json_data)
    if not res:
        result['result'] = 'NG'
        result['error'] = msg
    return result


@api.route('/note/like/<int:note_id>', methods=['get'])
def api_like_note(note_id):
    result = {'result': 'OK', 'error': ''}
    res, msg = NoteServer().like_note(note_id)
    if not res:
        result['result'] = 'NG'
        result['error'] = msg
    else:
        result['content'] = msg
    return result






