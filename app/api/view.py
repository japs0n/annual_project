#!/usr/bin/python
# -*- coding: UTF-8 -*-

from . import api
import requests
from app import db
from app.model import User, College
from flask import request, session, jsonify, send_from_directory
from app.modules.Calculator import Calculator
from app.modules.Catch_Page import Crawler
from app.modules.Course_info import NianDu


@api.route("/ehallLogin", methods=["POST"])
def ehall_login():
    req_msg = request.json
    number = req_msg.get("number", "")
    ehall_password = req_msg.get("password", "")
    user_obj = User.query.filter(User.Sno == number).filter(User.ehall_password == ehall_password).first()
    # 检查是否存在用户对象
    if user_obj is not None:
        # 检查是否存在已查询数据
        if user_obj.data != {}:
            session['has'] = True
            return jsonify(error=1, pic='Happy coding!')
        # 如果未获取数据则重新获取验证码
        session['password'] = user_obj.ecard_password
        session['name'] = user_obj.name
        session['check'] = True
        session['college'] = user_obj.college.name
        o = Crawler()
        pic = o.get_captcha()
        user_obj.pic = pic
        user_obj.ecard_cookie = requests.utils.dict_from_cookiejar(o.cookie)
        return jsonify(error=0, pic=user_obj.pic)
    else:
        # 尝试登陆信息门户
        check = NianDu.login(number, ehall_password)
        error_type1 = {
            "error_1": "首页请求失败",
            "error_2": "用户名/密码错误",
            "error_3": "模拟登陆异常",
            "error_4": "教务系统登陆异常",
        }
        if check in error_type1:
            return jsonify(error=error_type1[check])
        session['number'] = number
        # 尝试获取 姓名 消费记录查询密码 学院
        number_tuple = NianDu.number(check)
        error_type2 = {
            "error_5": "请求个人信息出现异常",
            "error_6": "个人信息处理出现异常"
        }
        if number_tuple in error_type2:
            return jsonify(error=error_type2[number_tuple])
        else:
            name, ecard_password, college = number_tuple
        session['password'] = ecard_password
        session['name'] = name
        session['check'] = True
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
        # 获取验证码
        o = Crawler()
        pic = o.get_captcha()
        college_obj = College.query.filter(College.name == college_s).first()
        if college_obj is None:
            return jsonify(error='学院不存在')
        ehall_cookie = requests.utils.dict_from_cookiejar(check.cookies)
        ecard_cookie = requests.utils.dict_from_cookiejar(o.cookie)
        user_obj = User(belong_college=college_obj.id, name=name, Sno=number, pic=pic, dict={},
                        ehall_cookie=ehall_cookie, ecard_cookie=ecard_cookie,
                        ehall_password=ehall_password, ecard_password=ecard_password)
        db.session.add(user_obj)
        db.session.commit()
        return jsonify(error=0, pic=pic)


@api.route("/ecardLogin", methods=["POST"])
def ecard_login():
    check = session.get('check', '')
    if (check is not True) or check == '':
        return jsonify(error='4')
    else:
        req_msg = request.json
        code = req_msg.get('code', '')
        _password = req_msg.get('password', '')
        number = session['number']
        password = session['password']
        password = password if _password == '' else _password
        user_obj = User.query.filter(User.Sno == number).filter(User.ecard_password == password).first()
        o = Crawler()
        o.cookie = requests.utils.cookiejar_from_dict(user_obj.ecard_cookie)
        login_status = o.login(code, number, password)
        session['auth'] = True if login_status == 0 else False
        return jsonify(error=login_status)


@api.route("/information", methods=["GET"])
def get_information():
    auth = session.get('auth', '')
    if auth is '' or auth is False:
        return jsonify(error=1)
    # 如果已查询过直接返回保存值
    user_obj = User.query.filter(User.Sno == session['number']).first()
    if session['has']:
        response = jsonify(user_obj.data) if user_obj else jsonify(error=2)
        return response
    # 还原教务系统cookie
    ehall_cookie = requests.utils.cookiejar_from_dict(user_obj.ehall_cookie)
    kebiao_tuple = NianDu.kebiao(ehall_cookie, session['number'])
    error_type = {
        "error_7": "请求课表页面出现异常",
        "error_8": "课表信息处理出现异常",
        "课表为空": "课表为空",
    }
    if kebiao_tuple in error_type:
        return jsonify(error=error_type[kebiao_tuple])
    else:
        term, courseCount, classCount, classDay, list3 = kebiao_tuple
    # 还原一卡通系统cookie
    o = Crawler()
    o.cookie = requests.utils.cookiejar_from_dict(user_obj.ecard_cookie)
    # 获取账户类型
    account_check = o.get_account()
    if account_check is not True:
        return jsonify(error=account_check)
    college_obj = College.query.filter(College.name == session['college']).first()
    if college_obj is None:
        return jsonify(error=3)
    ranking = college_obj.times + 1
    # 获取消费账单
    bill = o.get_bill()
    if not bill:
        return jsonify(error=4)
    # 对账单信息进行处理
    c = Calculator(bill)
    most_visit_place, most_visit_times = c.get_most_visit()
    info = {
        "name": session['name'],
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
    user_obj.data = info
    college_obj.times = ranking
    db.session.add(college_obj)
    db.session.add(user_obj)
    db.session.commit()
    return jsonify(info)


@api.route("/test/get_cookie")
def get_cookie():
    user_obj = User.query.filter(User.Sno == session['number']).first()
    return jsonify(ecard_cookie=user_obj.ecard_cookie, ehall_cookie=user_obj.ehall_cookie,
                   number=session['number'], ecard_password=session['password'], college=session['college'])


@api.route("/test/get_data")
def get_data():
    user_obj = User.query.filter(User.Sno == request.form['number']).first()
    response = jsonify(user_obj.data) if user_obj else jsonify(error=2)
    return response


@api.route('/<path:path>')
def get_resource(path):
    return send_from_directory('static', path)
