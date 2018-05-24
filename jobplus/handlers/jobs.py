from flask import Blueprint, render_template, current_app, request
from jobplus.models import JobInfo as Job

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
    return render_template('job/details.html',cjob=cjob)
