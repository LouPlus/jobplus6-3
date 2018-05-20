# coding:utf-8

from flask import Blueprint, render_template,flash
from flask import redirect,url_for
from jobplus.forms import CompanyForm
from jobplus.models import ComInfo
from flask_login import login_required,current_user

company = Blueprint('company', __name__, url_prefix='/company')

@company.route('/')
@login_required
def index():

    return render_template('company/index.html')


@company.route('/profile',methods=['GET','POST'])
@login_required
def setdetail():
    # 此处company的id需要从login获取
    company = ComInfo.query.get_or_404(current_user.id)
    form = CompanyForm(obj=company)
    
    if form.validate_on_submit():
        form.set_details(company)
        flash('更新信息成功!','success')
        return redirect(url_for('company.index'))
    return render_template('company/set_details.html',form=form)

