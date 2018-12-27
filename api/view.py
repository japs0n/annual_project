from . import api
import pickle
from ..model import User, College
from flask import request, session, jsonify
from ..modules.LoginSimulator import LoginSimulator
from ..modules.Catch_Page import Crawler
from ..modules.Course_info import NianDu


@api.route("/ehallLogin")
def ehall_login():
    req_msg = request.json
    number = req_msg.get("number", "")
    password = req_msg.get("password", "")
    check = NianDu.login(number, password)
    if not check:
        return jsonify(errror=1)
    session['number'] = number
    name, password, xueyuan = NianDu.process_number(check)
    session['password'] = password
    session['check'] = pickle.dumps(check)

    return jsonify(error=0, pic=pic)


@api.route("/ecardlogin")
def ecard_login():
    if session['check'] is None:
        return jsonify(error='未登陆教务系统')
    else:
        check = pickle.load(session['check'])
        password = session['password']
        req_msg = request.json
        code = req_msg.get('code', '')
        _password = req_msg.get('password', '')
        password = password if _password == '' else _password
        Crawler.login()
        return

@api.route("information")
def get_information():
    if session['auth'] is not True:
        return jsonify(error=1)
    else:
        pass
    return

