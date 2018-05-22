from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import url_for
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

db = SQLAlchemy()


class Base(db.Model):
    """ model基类，默认添加了时间戳 """
    # 表示不要把该类当作Model类
    __abstract__ = True
    # 设置自动维护的时间戳
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                default=datetime.utcnow,
                onupdate=datetime.utcnow)


class User(Base,UserMixin):
    """ 用户信息类 """
    __tablename__ = 'user'

    #角色分配
    ROLE_USER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(32),unique=True,index=True,nullable=False)
    email = db.Column(db.String(64),unique=True,index=True,nullable=False)

    #password 指定列名
    _password = db.Column('password',db.String(256),nullable=False)
    role = db.Column(db.SmallInteger,default=ROLE_USER)

    # 以下信息为用户补充信息
    realname = db.Column(db.String(32))
    resume = db.Column(db.String(128))
    phone = db.Column(db.String(12))
    exp = db.Column(db.String(24))

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,orig_password):
        """ 存入password """
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        """ 判断用户输入的密码和存储的hash密码是否相等 """
        return check_password_hash(self._password,password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY


class JobInfo(Base):
    """ 工作信息表 """
    __tablename__ = 'jobinfo'
    # 与compinfo表的关系为 1对多，一个company对应多个job

    job_id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(128),index=True,nullable=False)
    work_place = db.Column(db.String(128),nullable=False)

    tags = db.Column(db.String(128),nullable=True)
    desc = db.Column(db.String(256))
    high_salary = db.Column(db.Integer)
    low_salary = db.Column(db.Integer)
    exp = db.Column(db.Integer)
    degree = db.Column(db.String(24))
    # 上线标志，1-上线，0-下线
    isonline = db.Column(db.Boolean,default=1)

    # 关联到ComInfo表中的company
    comp_id = db.Column(db.Integer,db.ForeignKey('cominfo.com_id',ondelete='CASCADE'))
    company = db.relationship('ComInfo',uselist=False,backref=db.backref("job"))

    def __repr__(self):
        return '<Company:{},Job:{}>'.format(self.company.user.username,self.title)


class ComInfo(Base):
    """ 企业用户信息扩展表 """
    __tablename__ = 'cominfo'
    # 与user表的关系为 1对1
    com_id = db.Column(db.Integer,db.ForeignKey('user.id',ondelete='CASCADE'),primary_key=True)
    user = db.relationship('User',uselist=False,backref=db.backref("company"))

    com_phone = db.Column(db.String(11))
    com_location = db.Column(db.String(128))
    com_logo = db.Column(db.String(128))
    com_web = db.Column(db.String(64))
    com_desc_less = db.Column(db.String(128))
    com_desc_more = db.Column(db.String(256))

    def __repr__(self):
        return '<Company:{}>'.format(self.user.username)


class UserJob(Base):
    """ User表与JobInfo表的中间表 """
    __tablename__ = 'userjob'

    uj_id = db.Column(db.Integer,primary_key=True)

    # 与User表建立关系
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    user = db.relationship('User',backref=db.backref('interm'))

    # 与JobInfo表建立关系
    job_id = db.Column(db.Integer,db.ForeignKey('jobinfo.job_id'))
    job = db.relationship('JobInfo',backref=db.backref('interm'))

    # 简历状态 0-待查看，1-已拒绝，2-面试
    status = db.Column(db.SmallInteger,default=0)
