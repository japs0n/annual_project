# -*- coding: utf-8 -*-
import time
import random
import string
import hashlib
import urllib.request
import json
from config import config

wechatConfig = config.get('default', '').wechatConfig


class Token:
    def __init__(self, redirect_url=wechatConfig['redirect_url']):
        self.backUrl = self.__create_backUrl(redirect_url)

    def __create_backUrl(self, redirect_url=wechatConfig['redirect_url']):
        """创建回调网址"""
        return '''https://open.weixin.qq.com/connect/oauth2/authorize?
        appid={}&
        redirect_uri={}&
        response_type=code&
        scope={}&
        state=STATE#wechat_redirect
        '''.format(
            wechatConfig['appid'],
            redirect_url,
            wechatConfig['scope']
        ).replace(' ', '').replace('\n', '')

    def getToken(self, code):
        """获取网页授权Access_token"""
        req_str = urllib.request.urlopen('''https://api.weixin.qq.com/sns/oauth2/access_token?
            appid={}&
            secret={}&
            code={}&
            grant_type=authorization_code
            '''.format(wechatConfig['appid'], wechatConfig['secret'], code)
               .replace(' ', '').replace('\n', '')) \
            .read().decode('utf-8')
        req_dict = json.loads(req_str)
        return req_dict

    def getUser(self, access_token, openid):
        """用openid获取用户信息"""
        user_msg = urllib.request.urlopen('''https://api.weixin.qq.com/sns/userinfo?
            access_token={}&
            openid={}&
            lang=zh_CN
            '''.format(access_token, openid)
               .replace(' ', '').replace('\n', '')) \
            .read().decode('utf-8')
        user_msg = json.loads(user_msg)
        return user_msg


class Sign:
    def __init__(self, url):
        self.config = {
            'timestamp': self.__create_timestamp(),
            'nonceStr': self.__create_nonceStr(),
            'url': url
        }

    def __create_timestamp(self):
        return int(time.time())

    def __create_nonceStr(self):
        return ''.join(random.choice(
            string.ascii_letters + string.digits) for _ in range(15))

    def sign(self, access_token):
        jsapi_ticket = urllib.request.urlopen('''
            https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={}&type=jsapi
            '''.format(access_token).replace(' ', '').replace('\n', ''))\
            .read().decode('utf-8')
        self.config['jsapi_ticket'] = json.loads(jsapi_ticket)['ticket']
        tempStr = '&'.join(['{}={}'.format(
            key.lower(),
            self.config[key]) for key in sorted(self.config)])
        self.config['signature'] = hashlib.sha1(tempStr.encode()).hexdigest()
        self.config['appid'] = wechatConfig['appid']
        return self.config
