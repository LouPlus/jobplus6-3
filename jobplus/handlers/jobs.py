from flask import Blueprint, render_template, current_app, request
from jobplus.models import JobInfo as Job
from flask_login import current_user,login_required
from jobplus.models import UserJob,db
from flask import redirect,url_for,flash

jobs = Blueprint('jobs', __name__, url_prefix='/job')


# 职位列表
@jobs.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Job.query.order_by(Job.created_at.desc()).paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )
    return render_template('job/index.html', pagination=pagination, active='jobs')


# 职位详情
@jobs.route('/<int:job_id>')
def job_details(job_id):
    #cjob = Job.query.filter(Job.job_id == job_id)
    cjob = Job.query.get_or_404(job_id)
    deliv = UserJob.query.filter(UserJob.user_id==current_user.id,UserJob.job_id==job_id).first()
    if deliv:
        print('delivery id:%s'%deliv.uj_id)
    return render_template('job/details.html',cjob=cjob,d=deliv)

# 投递岗位
@jobs.route('/<int:job_id>/apply')
@login_required
def delivery(job_id):
    cjob = Job.query.get_or_404(job_id)
    uj = UserJob(user=current_user,job=cjob,resume=current_user.resume)
    db.session.add(uj)
    db.session.commit()
    flash('投递成功！','success')
    return redirect(url_for('jobs.job_details',job_id=job_id))
