# coding:utf-8

from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from jobplus.forms import CompanyForm
from jobplus.models import ComInfo
from flask_login import login_required, current_user

company = Blueprint('company', __name__, url_prefix='/company')

@company.route('/')
def index():
    # 获取参数中传过来的页面
    page = request.args.get('page', default=1, type=int)
    # 生成分页对象
    pagination = ComInfo.query.paginate(
        page=page,
        per_page=current_app.config['COMINFO_PER_PAGE'],
        error_out=False
    )
    return render_template('company/index.html', pagination=pagination)


@company.route('/profile',methods=['GET','POST'])
@login_required
def setdetail():
    # 此处company的id需要从login获取
    com_tmp = ComInfo.query.get_or_404(current_user.id)
    form = CompanyForm(obj=com_tmp)
    form.com_name.data = current_user.username
    form.com_email.data = current_user.email
    
    if form.validate_on_submit():
        form.set_details(current_user,com_tmp)
        flash('更新信息成功!','success')
        return redirect(url_for('company.index'))
    return render_template('company/set_details.html',form=form)

@company.route('/<int:company_id>')
def details(company_id):
    company = ComInfo.query.get_or_404(company_id)
    return render_template('company/details.html',company=company)
