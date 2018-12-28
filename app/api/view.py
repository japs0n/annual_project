from . import api
import pickle
import requests
from app import db
from app.model import User, College
from flask import request, session, jsonify
from app.modules.Calculator import Calculator
from app.modules.Catch_Page import Crawler
from app.modules.Course_info import NianDu


@api.route("/ehallLogin")
def ehall_login():
    req_msg = request.json
    number = req_msg.get("number", "")
    password = req_msg.get("password", "")
    check = NianDu.login(number, password)
    if not check:
        return jsonify(errror=1)
    session['number'] = number
    name, password, college = NianDu.number(check)
    trans = {
        '法学院': '法学院',
        '文学与新闻传播学院': '文传学院',
        '美术学院': '美术学院',
        '民族学与社会学学院': '民社学院',
        '外语学院': '外语学院',
        '经济学院': '经济学院',
        '管理学院': '管理学院',
        '公共管理学院': '公管学院',
        '教育学院': '教育学院',
        '马克思主义学院': '马克思学院',
        '计算机科学学院': '计科学院',
        '数学与统计学学院': '数统学院',
        '电子信息工程学院': '电信学院',
        '生物医学工程学院': '生医学院',
        '化学与材料科学学院': '化材学院',
        '资源与环境学院': '资环学院',
        '生命科学学院': '生科学院',
        '药学院': '药学院',
        '预科教育学院': '预科学院',
        '体育学院': '体育学院',
        '音乐舞蹈学院': '音舞学院',
    }
    college_s = trans[college]
    session['password'] = password
    session['check'] = pickle.dumps(check)
    session['college'] = college_s
    o = Crawler()
    pic = o.get_captcha()
    session['cookie'] = o.get_cookie()
    return jsonify(error=0, pic=pic)


@api.route("/ecardlogin")
def ecard_login():
    if session['check'] is None:
        return jsonify(error='未登陆教务系统')
    else:
        number = session['number']
        password = session['password']
        req_msg = request.json
        code = req_msg.get('code', '')
        _password = req_msg.get('password', '')
        password = password if _password == '' else _password
        o = Crawler()
        o.cookie = requests.utils.cookiejar_from_dict(session['cookie'])
        login_status = o.login(code, number, password)
        if login_status == 0:
            session['auth'] = True
        return jsonify(error=login_status)


@api.route("information")
def get_information():
    if not session['auth']:
        return jsonify(error=1)
    check = pickle.loads(session['check'])
    term, courseCount, classCount, classDay, list3 = NianDu.kebiao(check, session['number'])
    o = Crawler()
    o.cookie = requests.utils.cookiejar_from_dict(session['cookie'])
    if not o.get_account():
        return jsonify(error=2)
    college_obj = College.query.filter(College.name == session['college'])
    if college_obj is None:
        return jsonify(error=3)
    ranking = len(college_obj.users.all()) + 1
    c = Calculator(o.get_bill())
    info = {"type_count": c.get_type_count(),
            "times": c.times,
            "bf_times": c.bf_times,
            "bus_times": c.bus_times,
            "sum_price": c.sum_price,
            "hosp_times": c.hosp_times,
            "top_price_place": c.top_record[4].rstrip(),
            "top_price": c.sum_price,
            "ranking": ranking,
            "most_class": list3,
            "courseCount": courseCount,
            "classCount": classCount,
            "classDay": classDay,
            "term": term,
            }
    user_obj = User(belong_college=college_obj.id, Sno=session['number'], data=info)
    db.session.add(user_obj)
    db.session.commit()
    return jsonify(info)
