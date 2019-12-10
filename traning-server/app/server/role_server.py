from config import db
from flask import current_app
from app.db_models.models import Roles, UserRole


class RoleServer(object):
    def __init__(self, user_id):
        self.user_id = user_id
        self.role_list = []
        qs = db.session.query(UserRole).filter(UserRole.user_id == self.user_id).filter(UserRole.model_id.is_(None))
        for q in qs:
            if q.role_id not in self.role_list:
                self.role_list.append(q.role_id)

    def is_admin(self):
        """判断是否是管理员"""
        current_obj = current_app._get_current_object()
        admin_role = current_obj.config['ADMIN_ROLE_ID']
        if admin_role in self.role_list:
            return True
        else:
            return False

    def is_moderator(self):
        """判断是否是版主"""
        current_obj = current_app._get_current_object()
        moderator_role = current_obj.config['MODERATOR_ROLE_ID']
        if moderator_role in self.role_list:
            return True
        else:
            return False

    def is_model_moderator(self, model_id):
        """判读是否是该版块的版主"""
        current_obj = current_app._get_current_object()
        moderator_role = current_obj.config['MODERATOR_ROLE_ID']
        q = (db.session.query(UserRole).filter(UserRole.user_id == self.user_id)
             .filter(UserRole.role_id == moderator_role)
             .filter(UserRole.model_id == model_id).first())
        if q:
            return True
        else:
            return False

    def add_user_role(self, user_id, role_id):
        user_role = {
            UserRole.user_id.name: user_id,
            UserRole.role_id.name: role_id
        }
        db.session.add(UserRole(**user_role))

    def del_user_role(self, user_id, role_id):
        (db.session.query(UserRole).filter(UserRole.user_id == user_id)
         .filter(UserRole.role_id == role_id)
         .filter(UserRole.model_id.is_(None))
         .delete())



