#!/usr/bin/python
# -*- coding: UTF-8 -*-

from . import api
import pickle
import requests
from app import db
from app.model import User, College
from flask import request, session, jsonify
from app.modules.Calculator import Calculator
from app.modules.Catch_Page import Crawler
from app.modules.Course_info import NianDu


@api.route("/ehallLogin", methods=["POST"])
def ehall_login():
    req_msg = request.json
    number = req_msg.get("number", "")
    password = req_msg.get("password", "")
    # 尝试登陆信息门户
    check = NianDu.login(number, password)
    error_type1 = {
        "error_1": "首页请求失败",
        "error_2": "用户名/密码错误",
        "error_3": "模拟登陆异常",
        "error_4": "教务系统登陆异常",
    }
    if check in error_type1:
        return jsonify(error=error_type1[check])
    session['number'] = number
    # 尝试获取 姓名 学号 学院
    number_tuple = NianDu.number(check)

    error_type2 = {
        "error_5": "请求个人信息出现异常",
        "error_6": "个人信息处理出现异常"
    }
    if number_tuple in error_type2:
        return jsonify(error=error_type2[number_tuple])
    else:
        name, password, college = number_tuple
    session['password'] = password
    session['check'] = pickle.dumps(check)
    # 转换学院名称缩写
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
    session['college'] = college_s
    o = Crawler()
    pic = o.get_captcha()
    session['cookie'] = o.get_cookie()
    return jsonify(error=0, pic=pic)


@api.route("/ecardLogin", methods=["POST"])
def ecard_login():
    check = session.get('check', '')
    if (check is None)or check == '':
        return jsonify(error='4')
    else:
        req_msg = request.json
        code = req_msg.get('code', '')
        _password = req_msg.get('password', '')
        number = session['number']
        password = session['password']
        password = password if _password == '' else _password
        o = Crawler()
        o.cookie = requests.utils.cookiejar_from_dict(session['cookie'])
        login_status = o.login(code, number, password)
        user_obj = User.query.filter(User.Sno == number).first()
        session['has'] = True if user_obj else False
        session['auth'] = True if login_status == 0 else False
        return jsonify(error=login_status)


@api.route("/information", methods=["GET"])
def get_information():
    if not session['auth']:
        return jsonify(error=1)
    # 如果已查询过直接返回保存值
    if session['has']:
        user_obj = User.query.filter(User.Sno == session['number']).first()
        response = jsonify(user_obj.data) if user_obj else jsonify(error=2)
        return response
    # 还原教务系统cookie
    check = pickle.loads(session['check'])
    kebiao_tuple = NianDu.kebiao(check, session['number'])
    error_type = {
        "error_7": "请求课表页面出现异常",
        "error_8": "课表信息处理出现异常"
    }
    if kebiao_tuple in error_type:
        return jsonify(error=error_type[kebiao_tuple])
    else:
        term, courseCount, classCount, classDay, list3 = kebiao_tuple
    o = Crawler()
    o.cookie = requests.utils.cookiejar_from_dict(session['cookie'])
    account_check = o.get_account()
    if account_check is not True:
        return jsonify(error=account_check)
    college_obj = College.query.filter(College.name == session['college']).first()
    if college_obj is None:
        return jsonify(error=3)
    ranking = college_obj.times + 1
    bill = o.get_bill()
    if not bill:
        return jsonify(error=4)
    c = Calculator(bill)
    most_visit_place, most_visit_times = c.get_most_visit()
    info = {
        "ranking": ranking,
        "type_count": c.get_type_count(),
        "times": c.times,
        "bf_times": c.bf_times,
        "bus_times": c.bus_times,
        "sum_price": float(c.sum_price.copy_abs()),
        "hosp_times": c.hosp_times,
        "top_price_place": c.top_record[4].rstrip(),
        "most_visit_place": most_visit_place,
        "most_visit_times": most_visit_times,
        "top_price": float(c.top_price.copy_abs()),
        "overdue_times": c.overdue_times,
        "overdue_price": float(c.overdue_price.copy_abs()),
        "courseCount": courseCount,
        "classCount": classCount,
        "classDay": classDay,
        "most_class": list3,
        "term": term,
        "college": session['college'],
    }
    user_obj = User(belong_college=college_obj.id, Sno=session['number'], data=info)
    college_obj.times = ranking
    db.session.add(college_obj)
    db.session.add(user_obj)
    db.session.commit()
    return jsonify(info)


@api.route("/test/get_cookie")
def get_cookie():
    return jsonify(session=session['cookie'], number=session['number'],
                   password=session['password'], college=session['college'])
