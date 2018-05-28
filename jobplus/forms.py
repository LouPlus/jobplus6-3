# *_*coding:utf-8 *_*
import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import TextAreaField,IntegerField
from wtforms.validators import Length,Email,EqualTo,Required,URL,NumberRange
from wtforms import ValidationError
from jobplus.models import User,JobInfo,ComInfo,db
from flask_wtf.file import FileField, FileRequired

class CompanyForm(FlaskForm):
    com_name = StringField('企业名称',validators=[Required(),Length(3,24)])
    com_email = StringField('邮箱',validators=[Required(),Email()])
    password = StringField('密码(不填保持原密码不变)')
    com_location = StringField('地址', validators=[Required(), Length(1, 24)])
    com_logo = StringField('logo链接',validators=[Required(),URL()])
    com_web = StringField('网站链接',validators=[Required(),URL()])
    com_phone = StringField('手机号码', validators=[Required()])
    com_desc_less = StringField('一句话简介',validators=[Required(),Length(3,48)])
    com_desc_more = TextAreaField('详细介绍', validators=[Required(), Length(3, 256)])
    submit = SubmitField('提交')

    def set_details(self, usr, com):
        # 将表单数据填入数据库映射类对象
        usr.username = self.com_name.data
        usr.email = self.com_email.data
        if self.password.data:
            usr.password = self.password.data

        db.session.add(usr)
        db.session.commit()

        self.populate_obj(com)
        com.com_location = self.com_location.data
        com.com_logo = self.com_logo.data
        com.com_web = self.com_web.data
        com.com_desc_less = self.com_desc_less.data
        com.com_desc_more = self.com_desc_more.data
        com.com_phone = self.com_phone.data

        db.session.add(com)
        db.session.commit()
        return com

    # 需要验证邮箱唯一性？(需要再添加)
    # 验证密码长短
    def validate_password(self, field):
        if field.data and not re.match(r'^[a-zA-Z0-9]{6,24}$', field.data):
            raise ValidationError('请输入6至24位字母或者数字!')

    # 验证手机号码
    def validate_com_phone(self, field):
        if field.data and not re.match(r'^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$',
                                       field.data):
            raise ValidationError('请输入正确手机号!')


class UserForm(FlaskForm):
    realname = StringField('姓名', validators=[Required(), Length(1, 24)])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码')
    # 手机号需补充验证
    phone = StringField('手机号', validators=[Required()])
    exp = StringField('工作经验', validators=[Length(0, 24)])
    # 简历先用url代替
    resume = StringField('简历', validators=[Required(), URL()])
    submit = SubmitField('提交')

    def set_info(self, user):
        # self.populate_obj(user)
        user.realname = self.realname.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data
        user.phone = self.phone.data
        user.exp = self.exp.data
        user.resume = self.resume.data

        db.session.add(user)
        db.session.commit()
        return user


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[Required(message='* 用户名不能为空'), Length(3, 24, message='用户名长度要在3～24个字符之间')])
    email = StringField('邮箱', validators=[Required(message='* 邮箱不能为空'), Email(message='邮箱名不合法')])
    password = PasswordField('密码', validators=[Required(message='* 密码不能为空'), Length(6, 24, message='密码长度要在6～24个字符之间')])
    repeat_password = PasswordField('确认密码', validators=[Required(message='* 密码不能为空'),
                                                        EqualTo('password', message='两次填写的密码不一致')])
    submit = SubmitField('提交')

  
    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user

    def validate_username(self, field):
        """ 验证用户名是否已存在 """
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已注册')

    def validate_email(self, field):
        """ 验证用户邮箱是否已存在 """
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已注册')


    
class LoginForm(FlaskForm):
    username_or_email = StringField('用户名/邮箱', validators=[Required(message='* 用户名/邮箱不能为空')])
    password = PasswordField('密码', validators=[Required(message='* 密码不能为空'), Length(6, 24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_username_or_email(self, field):
        """ 验证是否为合法的邮箱名或用户 """
        pattern = '\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+.)+[A-Za-z]{2,14}'
        if re.match(pattern, field.data):
            if not User.query.filter_by(email=field.data).first():
                raise ValidationError('该邮箱未注册')
        else:
            if not User.query.filter_by(username=field.data).first():
                raise ValidationError('该用户不存在')

    def validate_password(self, field):
        user = User.query.filter_by(email=self.username_or_email.data).first()
        if not user:
            user = User.query.filter_by(username=self.username_or_email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')


class RegisterComForm(FlaskForm):
    companyname = StringField('用户名', validators=[Required(message='* 用户名不能为空')])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField('重复密码', validators=[Required(), EqualTo('password')])
    submit = SubmitField('提交')

    def create_company(self):
        user = User()
        user.username = self.companyname.data
        user.email = self.email.data
        user.password = self.password.data
        user.role = User.ROLE_COMPANY

        db.session.add(user)
        db.session.commit()

        company = ComInfo()
        company.user = user

        db.session.add(company)
        db.session.commit()

    def validate_companyname(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("用户名已经存在！")
        if not re.match(r'^[a-zA-Z0-9]{3,24}$', field.data):
            raise ValidationError('请输入3至24位字母或数字！')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已注册！')


class Add_UserForm(FlaskForm):
    username = StringField('用户名', validators=[Required(message='* 用户名不能为空'), Length(3, 24, message='用户名长度要在3～24个字符之间')])
    email = StringField('邮箱', validators=[Required(message='* 邮箱不能为空'), Email(message='邮箱名不合法')])
    password = PasswordField('密码', validators=[Required(message='* 密码不能为空'), Length(6, 24, message='密码长度要在6～24个字符之间')])
    phone = StringField('手机号', validators=[Required()])

    submit = SubmitField('提交')

    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        user.phone = self.password.data
        db.session.add(user)
        db.session.commit()
        return user

    def validate_username(self, field):
        """ 验证用户名是否已存在 """
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已注册')

    def validate_email(self, field):
        """ 验证用户邮箱是否已存在 """
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已注册')


class Add_ComForm(FlaskForm):
    companyname = StringField('企业名称', validators=[Required(message='* 用户名不能为空')])
    email = StringField('邮箱', validators=[Required(), Email()])
    password = PasswordField('密码', validators=[Required(), Length(6, 24)])
    com_web = StringField('网站链接', validators=[Required(), URL()])
    com_desc_less = StringField('一句话简介', validators=[Required(), Length(3, 48)])

    submit = SubmitField('提交')

    def create_company(self):
        user = User()
        user.username = self.companyname.data
        user.email = self.email.data
        user.password = self.password.data
        user.role = User.ROLE_COMPANY

        db.session.add(user)
        db.session.commit()

        company = ComInfo()
        company.user = user
        company.com_web = self.com_web.data
        company.com_desc_less = self.com_desc_less.data

        db.session.add(company)
        db.session.commit()

    def validate_companyname(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("用户名已经存在！")
        if not re.match(r'^[a-zA-Z0-9]{3,24}$', field.data):
            raise ValidationError('请输入3至24位字母或数字！')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已注册！')



class UploadForm(FlaskForm):
    file = FileField(validators=[FileRequired('文件未选择!')])
    submit = SubmitField('上传')
