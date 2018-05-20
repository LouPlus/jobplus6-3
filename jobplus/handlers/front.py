import re
from flask import Blueprint, render_template, url_for, flash, redirect
from jobplus.forms import LoginForm, RegisterForm,RegisterComForm
from flask_login import login_user
from jobplus.models import User


front = Blueprint('front', __name__)

# 首页路由函数
@front.route('/')
def index():
    return render_template('index.html')


# 登录视图函数
@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    pattern = '\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+.)+[A-Za-z]{2,14}'
    if form.validate_on_submit():
        if re.match(pattern, form.username_or_email.data):
            user = User.query.filter_by(email=form.username_or_email.data).first()
        else:
            user = User.query.filter_by(username=form.username_or_email.data).first()
        login_user(user, form.remember_me.data)
        # 这里后面要填写定向到哪个页面
        return 'Login Success'
    return render_template('login.html', form=form)


# 注册视图函数
@front.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录！', 'success')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)

# 企业注册函数
@front.route('/registercom',methods=['GET','POST'])
def register_com():
    form = RegisterComForm()
    if form.validate_on_submit():
        form.create_company()
        flash('注册成功，请登录！','success')
        return redirect(url_for('front.login'))
    return render_template('register_com.html',form=form)
