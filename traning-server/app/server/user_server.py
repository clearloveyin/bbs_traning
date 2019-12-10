from flask import current_app
from config import db
from app.db_models.models import Users
from app.db_models.models import UserRole
from app.db_models.models import Notes
from app.db_models.models import Issue
from app.db_models.models import Roles
from app.server.role_server import RoleServer


class UserServer(object):
    def __init__(self):
         pass

    def login(self, **kwargs):
        """用户登陆"""
        username = kwargs.get('username')
        password = kwargs.get('password')
        user_dict = self.get_user(username)
        if password == user_dict.get('password'):
            return True, user_dict
        else:
            return False, '用户名或密码错误！'

    def sign(self, **kwargs):
        """用户注册"""
        user_name = kwargs.get('username')
        password = kwargs.get('password')
        if user_name and password:
            res, msg = self.add_user(user_name, password)
            db.session.commit()
            return res, msg
        else:
            return False, '用户名或密码不能为空！'

    def get_user(self, user_name):
        """根据名字获取用户信息"""
        q = db.session.query(Users).filter(Users.user_name == user_name).first()
        if q:
            user_dict = q.to_dict()
            return user_dict
        else:
            return dict()

    def add_user(self, user_name, password):
        """添加新用户"""
        if not self.get_user(user_name):
            user_dict = {'user_name': user_name,
                         'password': password}
            new_user = Users(**user_dict)
            db.session.add(new_user)
            return True, ''
        else:
            return False, '该用户已存在！'

    def del_user(self, user_id):
        """删除用户"""
        q = (db.session.query(UserRole)
             .filter(UserRole.user_id == user_id)
             .filter(UserRole.model_id.isnot(None))
             .first())
        if q:
            return False, "该用户下有版块，无法删除！"
        else:
            db.session.query(UserRole).filter(UserRole.user_id == user_id).delete()
            db.session.query(Notes).filter(Notes.user_id == user_id).delete()
            db.session.query(Issue).filter(Issue.user_id == user_id).delete()
            db.session.query(Users).filter(Users.user_id == user_id).delete()
        db.session.commit()
        return True, ""

    def get_user_list(self, user_id):
        """获取所有用户"""
        role_server = RoleServer(user_id)
        is_admin = role_server.is_admin()
        if not is_admin:
            return False, '您不是管理员，没有权限查看管理员页面！'
        user_list = []
        qs = (db.session.query(Users.user_id, Users.user_name)
              .order_by(Users.user_name)
              )
        for q in qs:
            user_dict = dict()
            user_dict['user_id'] = q[0]
            user_dict['user_name'] = q[1]
            role_dict = self.get_user_role(q[0])
            role_id_list = []
            role_name_list = []
            for key, val in role_dict.items():
                role_id_list.append(key)
                role_name_list.append(val)
            user_dict['role_id_list'] = role_id_list
            user_dict['role_names'] = ';'.join(role_name_list)
            user_list.append(user_dict)
        return True, user_list

    def get_user_role(self, user_id):
        role_dict = dict()
        qs = (db.session.query(UserRole.role_id, Roles.role_name)
              .outerjoin(Roles, UserRole.role_id == Roles.role_id)
              .filter(UserRole.model_id.is_(None))
              .filter(UserRole.user_id == user_id).distinct())
        for q in qs:
            role_dict[q[0]] = q[1]
        return role_dict

    def assign_user_role(self, **kwargs):
        """分配用户角色"""
        try:
            current_obj = current_app._get_current_object()
            user_id = kwargs.get('user_id')
            boolean_admin = kwargs.get('admin')
            boolean_moderator = kwargs.get('moderator')
            role_server = RoleServer(user_id)
            is_admin = role_server.is_admin()
            is_moderator = role_server.is_moderator()
            if boolean_admin:
                if not is_admin:
                    role_server.add_user_role(user_id, current_obj.config['ADMIN_ROLE_ID'])
            else:
                if is_admin:
                    role_server.del_user_role(user_id, current_obj.config['ADMIN_ROLE_ID'])
            if boolean_moderator:
                if not is_moderator:
                    role_server.add_user_role(user_id, current_obj.config['MODERATOR_ROLE_ID'])
            else:
                if is_moderator:
                    role_server.del_user_role(user_id, current_obj.config['MODERATOR_ROLE_ID'])
            db.session.commit()
            return True, ''
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s', str(e))
            return False, str(e)

    def update_user(self, user_id, **kwargs):
        """更新用户信息"""
        try:
            user_name = kwargs.get('user_name')
            old_password = kwargs.get('old_password')
            new_password = kwargs.get('new_password')
            q = db.session.query(Users).filter(Users.user_id == user_id)
            if old_password != q.first().password:
                return False, '旧密码输入错误！'
            if new_password:
                user_update = {"user_name": user_name, "password": new_password}
            else:
                user_update = {"user_name": user_name}
            q.update(user_update)
            db.session.commit()
            return True, ''
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s', str(e))
            return False, str(e)




