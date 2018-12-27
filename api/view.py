from . import api
import pickle
from ..model import User, College
from flask import request, session, jsonify
from ..modules.Catch_Page import Crawler
from ..modules.Course_info import NianDu


@api.route("/ehallLogin")
def ehall_login():
    req_msg = request.json
    number = req_msg.get("number", "")
    password = req_msg.get("number", "")
    check = NianDu.login(number,password)
    if check

    return


@api.route("/ecardlogin")
def ecard_login():
    req_msg = request.json
    req_msg.get('code')

@api.route("information")
def get_information():
    if session['auth'] is not True:
        return jsonify(error='1')
    else:

