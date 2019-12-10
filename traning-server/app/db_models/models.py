from ..db_models import db
from sqlalchemy.orm import relationship
import datetime


# 角色表
class Roles(db.Model):
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(100), unique=True, index=True)  # 管理员/版主/普通用户

    def __repr__(self):
        return '<Role %r>' % self.role_name

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


# 用户表
class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __repr__(self):
        return '<user_name:%r>' % self.user_name

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


# 板块表
class Models(db.Model):
    __tablename__ = 'models'
    model_id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(100), index=True)
    create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<model_name:%r>' % self.model_name

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if isinstance(attr, datetime.datetime) or isinstance(attr, datetime.time) or isinstance(attr, datetime.date):
                attr = attr.strftime("%Y-%m-%d %H:%M:%S")
            d[column.name] = attr
        return d


# 帖子表
class Notes(db.Model):
    __tablename__ = 'notes'
    note_id = db.Column(db.Integer, primary_key=True)
    note_name = db.Column(db.String(100), index=True)
    content = db.Column(db.String(1024))
    top = db.Column(db.BOOLEAN, default=False)  # True:置顶，加精
    like_num = db.Column(db.Integer)  # 点赞数
    create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    model_id = db.Column(db.Integer, db.ForeignKey('models.model_id'))

    issues = relationship("Issue", backref="note")

    def __repr__(self):
        return '<note_name:%r>' % self.note_name

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if isinstance(attr, datetime.datetime) or isinstance(attr, datetime.time) or isinstance(attr, datetime.date):
                attr = attr.strftime("%Y-%m-%d %H:%M:%S")
            d[column.name] = attr
        return d


# 用户角色表
class UserRole(db.Model):
    __tablename__ = 'user_role'

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    model_id = db.Column(db.Integer, db.ForeignKey('models.model_id'))

    def __repr__(self):
        return '<id:%r>' % self.id

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


db.Index('user_role_model_id_idx',
         UserRole.role_id, UserRole.user_id,
         UserRole.model_id,
         unique=True
         )


# 评论表
class Issue(db.Model):
    __tablename__ = 'issue'

    issue_id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(100))
    parent_id = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    note_id = db.Column(db.Integer, db.ForeignKey('notes.note_id'))
    create_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if isinstance(attr, datetime.datetime) or isinstance(attr, datetime.time) or isinstance(attr, datetime.date):
                attr = attr.strftime("%Y-%m-%d %H:%M:%S")
            d[column.name] = attr
        return d
