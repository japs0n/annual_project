from urllib import error, parse, request
from base64 import b64encode, b64decode
from http import cookiejar
from random import random
from lxml import etree
import json

LOGIN_URL = 'http://ecard.scuec.edu.cn/loginstudent.action'
CAPTCHAURL = "http://ecard.scuec.edu.cn/homeLogin.action/getCheckpic.action?rand=" + str(random() * 10000)


# TOPURL = 'http://ecard.scuec.edu.cn/pages/top.jsp'


def save_img(o):
    imagedata = b64decode(o.get_captcha())
    file = open('1.jpg', "wb")
    file.write(imagedata)
    file.close()


class LoginSimulator:
    cookie = cookiejar.CookieJar()

    def __init__(self, LoginUrl, CaptchaUrl):
        """
        构造函数
        :param LoginUrl:登陆链接
        :param CaptchaUrl: 获取验证码链接
        """
        self.LoginUrl = LoginUrl
        self.CaptchaUrl = CaptchaUrl
        # 托管整个生命周期cookie
        self.opener = request.build_opener(request.HTTPCookieProcessor(self.cookie))

    def get_captcha(self):
        """
        获取cookie=>SessionID
        :return: base64编码的验证码图片
        """
        return b64encode(self.opener.open(self.CaptchaUrl).read())

    def login(self, rand, name, password):
        postData = {
            'name': name,
            'userType': '1',
            'passwd': password,
            'loginType': '2',
            'rand': rand,
            'imageField.x': '22',
            'imgaeField.y': '21'
        }
        headers = {
            'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image \
            / apng, * / *;q = 0.8',
            'Host': 'ecard.scuec.edu.cn',
            'Referer': 'http://ecard.scuec.edu.cn/homeLogin.action',
            'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit \
            / 537.36(KHTML, likeGecko) Chrome / 67.0.3396.99Safari / 537.36'
        }
        # 发送登陆数据
        postdata = parse.urlencode(postData)
        req = request.Request(self.LoginUrl, postdata.encode(), headers)
        try:
            res = self.opener.open(req)
        except error.URLError as e:
            return False
        res = res.read().decode('gb2312')
        tree = etree.HTML(res)
        result = tree.xpath('//p[@class="biaotou"]')
        if len(result) < 1:
            return 0
        else:
            content_text = result[0].text
            if content_text == '登陆失败，密码错误':
                return 1
            elif content_text == '验证码错误，登陆失败':
                return 2
            elif content_text == '登陆失败，无此用户名称！':
                return 3

    def get_cookie(self):
        json_str = json.dumps(LoginSimulator.cookie)
        return json_str
        # return LoginSimulator.cookie
