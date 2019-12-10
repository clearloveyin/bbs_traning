from config import db
import time
from flask import current_app
from app.db_models.models import Users
from app.db_models.models import Notes
from app.db_models.models import Issue
from app.server.role_server import RoleServer


class NoteServer(object):
    def __init__(self):
        pass

    def get_latest_notes(self):
        """获取最新的帖子"""
        note_list = []
        qs = (db.session.query(Notes, Users.user_name)
              .outerjoin(Users, Notes.user_id == Users.user_id)
              .order_by(Notes.create_time.desc()))
        for q in qs:
            note_dict = dict()
            note_dict["note_id"] = q.Notes.note_id
            note_dict['note_name'] = q.Notes.note_name
            note_dict['create_time'] = q.Notes.create_time.strftime("%Y-%m-%d %H:%M:%S")
            note_dict['create_user'] = q.user_name
            if q.Notes.top:
                note_dict['top'] = '精品贴'
            else:
                note_dict['top'] = '普通贴'
            note_dict['like_num'] = q.Notes.like_num
            note_dict['issue_num'] = len(q.Notes.issues)
            note_list.append(note_dict)
        return note_list

    def get_notes_order_by_top(self):
        note_list = []
        qs = (db.session.query(Notes, Users.user_name)
              .outerjoin(Users, Notes.user_id == Users.user_id)
              .order_by(Notes.top.desc(), Notes.create_time.desc()))
        for q in qs:
            note_dict = dict()
            note_dict["note_id"] = q.Notes.note_id
            note_dict['note_name'] = q.Notes.note_name
            note_dict['create_time'] = q.Notes.create_time.strftime("%Y-%m-%d %H:%M:%S")
            note_dict['create_user'] = q.user_name
            if q.Notes.top:
                note_dict['top'] = '精品贴'
            else:
                note_dict['top'] = '普通贴'
            note_dict['like_num'] = q.Notes.like_num
            note_dict['issue_num'] = len(q.Notes.issues)
            note_list.append(note_dict)
        return note_list

    def get_notes_order_by_like(self):
        note_list = self.get_latest_notes()
        note_list.sort(key=lambda k: k['like_num'], reverse=True)
        return note_list

    def get_notes_order_by_issue(self):
        note_list = self.get_latest_notes()
        note_list.sort(key=lambda k: k['issue_num'], reverse=True)
        return note_list

    def post_note(self, note_dict):
        """发布帖子"""
        try:
            new_note = {
                Notes.user_id.name: note_dict.get('user_id'),
                Notes.model_id.name: note_dict.get('model_id'),
                Notes.note_name.name: note_dict.get('note_name'),
                Notes.content.name: note_dict.get('content'),
                Notes.create_time.name: time.strftime("%Y-%m-%d %H:%M:%S"),
                Notes.like_num.name: 0,
            }
            db.session.add(Notes(**new_note))
            db.session.commit()
            return True, ''
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s', str(e))
            return False, str(e)

    def get_notes_by_model_id(self, model_id):
        """根据模块id来获取帖子"""
        note_list = []
        qs = (db.session.query(Notes, Users.user_name)
              .outerjoin(Users, Notes.user_id == Users.user_id)
              .filter(Notes.model_id == model_id)
              .order_by(Notes.top.desc(), Notes.create_time.desc()))
        for q in qs:
            note_dict = dict()
            note_dict["note_id"] = q.Notes.note_id
            note_dict['note_name'] = q.Notes.note_name
            note_dict['create_time'] = q.Notes.create_time.strftime("%Y-%m-%d %H:%M:%S")
            note_dict['create_user'] = q.user_name
            note_dict['like_num'] = q.Notes.like_num
            if q.Notes.top:
                note_dict['top'] = '精品贴'
            else:
                note_dict['top'] = '普通贴'
            note_dict['issue_num'] = len(q.Notes.issues)
            note_list.append(note_dict)
        return note_list

    def get_note_info(self, note_id):
        """帖子详情"""
        q = (db.session.query(Notes, Users.user_name)
             .outerjoin(Users, Notes.user_id == Users.user_id)
             .filter(Notes.note_id == note_id).first())
        if not q:
            return False, '该帖子已经不存在了！'
        note_dict = dict()
        note_dict[Notes.content.name] = q.Notes.content
        note_dict[Notes.create_time.name] = q.Notes.create_time.strftime("%Y-%m-%d %H:%M:%S")
        note_dict[Users.user_name.name] = q.user_name
        note_dict[Notes.like_num.name] = q.Notes.like_num
        note_dict['issue_list'] = self.get_note_issue_list(note_id)
        return True, note_dict

    def judge_put_note(self, user_id, model_id):
        """判断有没有置顶贴子和删除帖子的权限"""
        role_server = RoleServer(user_id)
        is_admin = role_server.is_admin()
        is_moderator = role_server.is_model_moderator(model_id)
        if is_admin or is_moderator:
            return True
        else:
            return False

    def top_note(self, **kwargs):
        """加精置顶帖子"""
        user_id = kwargs.get('user_id')
        model_id = kwargs.get('model_id')
        note_id = kwargs.get('note_id')
        status = kwargs.get('status')
        if not self.judge_put_note(user_id, model_id):
            return False, "您没有权限操作！"
        q = db.session.query(Notes).filter(Notes.note_id == note_id).first()
        if not q:
            return False, "该帖子已经不存在了！"
        q.top = status
        db.session.commit()
        return True, ""

    def del_note(self, **kwargs):
        """删除帖子"""
        user_id = kwargs.get('user_id')
        model_id = kwargs.get('model_id')
        note_id = kwargs.get('note_id')
        q = db.session.query(Notes).filter(Notes.note_id == note_id)
        note = q.first()
        if not note:
            return False, "该帖子已经不存在了！"
        if not self.judge_put_note(user_id, model_id) and note.user_id != int(user_id):
            return False, "您没有权限操作！"
        q.delete()
        db.session.commit()
        return True, ""

    def issue_note(self, **kwargs):
        """评论帖子"""
        user_id = kwargs.get('user_id')
        note_id = kwargs.get('note_id')
        comment = kwargs.get('comment')
        try:
            issue_dict = {
                Issue.user_id.name: user_id,
                Issue.note_id.name: note_id,
                Issue.comment.name: comment,
                Issue.create_time.name: time.strftime("%Y-%m-%d %H:%M:%S")
            }
            db.session.add(Issue(**issue_dict))
            db.session.commit()
            return True, ''
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s', str(e))
            return False, str(e)

    def get_note_issue_list(self, note_id):
        """获取帖子评论"""
        issue_list = []
        qs = (db.session.query(Issue, Users.user_name)
              .outerjoin(Users, Issue.user_id == Users.user_id)
              .filter(Issue.note_id == note_id)
              .order_by(Issue.create_time.desc()))
        for q in qs:
            issue_dict = dict()
            issue_dict['create_user'] = q.user_name
            issue_dict['create_time'] = q.Issue.create_time.strftime("%Y-%m-%d %H:%M:%S")
            issue_dict['comment'] = q.Issue.comment
            issue_list.append(issue_dict)
        return issue_list

    def like_note(self, note_id):
        """点赞帖子"""
        try:
            q = db.session.query(Notes).filter(Notes.note_id == note_id).first()
            like_num = q.like_num+1
            q.like_num = like_num
            db.session.commit()
            return True, like_num
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s', str(e))
            return False, str(e)








