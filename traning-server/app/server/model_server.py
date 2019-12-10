import time
from flask import current_app
from config import db
from app.db_models.models import Models
from app.db_models.models import UserRole
from app.db_models.models import Notes
from app.db_models.models import Issue
from app.server.role_server import RoleServer


class ModelServer(object):
    def __init__(self):
        pass

    def get_models(self):
        """获取所有的板块"""
        model_list = []
        qs = db.session.query(Models).order_by(Models.create_time)
        for q in qs:
            model_list.append(q.to_dict())
        return model_list

    def judge_add_model(self, user_id):
        """判断能否添加板块"""
        role_server = RoleServer(user_id)
        is_admin = role_server.is_admin()
        is_moderator = role_server.is_moderator()
        if is_admin or is_moderator:
            return True
        else:
            return False

    def judge_del_model(self, model_id, user_id):
        """判断能否删除该模块"""
        role_server = RoleServer(user_id)
        is_admin = role_server.is_admin()
        is_moderator = role_server.is_model_moderator(model_id)
        if is_admin or is_moderator:
            return True
        else:
            return False

    def add_model(self, **kwargs):
        try:
            model_name = kwargs.get('modelName')
            model_user = kwargs.get('userId')
            if not self.judge_add_model(model_user):
                return False, '您没有添加版块的权限！'
            q = db.session.query(Models).filter(Models.model_name == model_name).first()
            if q:
                return False, '该模块已存在，请勿重复添加！'
            create_time = time.strftime("%Y-%m-%d %H:%M:%S")
            model_id = self.insert_model(model_name, create_time)
            self.insert_model_user(model_id, model_user)
            db.session.commit()
            return True, ''
        except Exception as e:
            current_app.logger.error('%s', str(e))
            return False, str(e)

    def insert_model(self, model_name, create_time):
        model_dict = {
            Models.model_name.name: model_name,
            Models.create_time.name: create_time
        }
        new_model = Models(**model_dict)
        db.session.add(new_model)
        db.session.flush()
        return new_model.model_id

    def insert_model_user(self, model_id, user_id):
        current_obj = current_app._get_current_object()
        role_id = current_obj.config['MODERATOR_ROLE_ID']
        model_user = {
            UserRole.user_id.name: user_id,
            UserRole.model_id.name: model_id,
            UserRole.role_id.name: role_id
        }
        db.session.add(UserRole(**model_user))

    def delete_model_by_id(self, model_id, user_id):
        """删除一个模块"""
        try:
            if not self.judge_del_model(model_id, user_id):
                return False, "您没有权限删除该模块！"
            q = db.session.query(Notes).filter(Notes.model_id == model_id).all()
            if len(q):
                return False, "该版块还存在帖子，无法删除！"
            self._delete_model(model_id)
            return True, ""
        except Exception as e:
            current_app.logger.error('%s', str(e))
            return False, str(e)

    def _delete_model(self, model_id):
        db.session.query(UserRole).filter(UserRole.model_id == model_id).delete()
        db.session.query(Models).filter(Models.model_id == model_id).delete()
        db.session.commit()


