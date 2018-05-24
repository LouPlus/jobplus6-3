# coding:utf-8

from jobplus.models import db,User,ComInfo,JobInfo

def gen():
    db.create_all()
    user = User(username='shiyanlou',email='shiyanlou@163.com',password='123456',role=20)
    company = ComInfo(user=user,com_phone='15122302865',com_location="北京市朝阳长安街1号",com_logo="https://static.lagou.com/thumbnail_300x300/i/image/M00/3E/22/CgqKkVdzobeAB7eoAAIUnE7Fe1M567.png",com_web="http://www.shiyanlou.com",com_desc_less="领先的互联网在线教育网站",com_desc_more="本来想粘贴过来，结果都是乱马，现在只好自己打一些字当作是详细介绍，但是又不知道到些什么内容好，只好瞎敲，看来好像也差不多了，再多打来两行吧，显得专业一点，行了，差不多了，就这些，这就是详细介绍！")
    job1 = JobInfo(title="Python工程师",work_place="北京市海淀区",tags="加班，加班",desc="需要掌握造火箭的全部技能，工作内容是在所有东西弄得差不多了之后，在火箭发射台的入口出的那个小门那里把门上的螺丝拧紧一些，省得每老是自己被风吹开了，ok，就这些！",high_salary=10000,low_salary=800,exp=5,degree="博士",company=company)
    job2 = JobInfo(title="测试工程师",work_place="天津市南开区",tags="加班，加班，加班",desc="同样需要掌握造火箭的全部技能，工作内容是在所有东西弄得差不多了之后，在上一个岗位的人员火箭发射台的入口出的那个小门那里把门上的螺丝拧紧一些之后，去检查一遍螺丝是否拧好了",high_salary=10000,low_salary=800,exp=5,degree="博士",company=company)
    db.session.add(user)
    db.session.commit()

    db.session.add(company)
    db.session.commit()

    db.session.add(job1)
    db.session.add(job2)
    db.session.commit()

