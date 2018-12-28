#!/usr/bin/python
# -*- coding: UTF-8 -*-

from .LoginSimulator import LoginSimulator
from urllib import parse
import requests
from lxml import etree
import re


class Crawler(LoginSimulator):
    def __init__(self):
        super().__init__()
        self.headers = dict(
            get={
                'Host': 'ecard.scuec.edu.cn',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\
                       /537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
                'Referer': 'http://ecard.scuec.edu.cn/accleftframe.action'
            },
            post1={
                'Host': "ecard.scuec.edu.cn",
                'Referer': "http://ecard.scuec.edu.cn/accounthisTrjn.action",
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\
                /537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
                'Connection': "keep-alive",
                'Content-Type': "application/x-www-form-urlencoded",
                'Content-Length': "52",
                'cache-control': "no-cache",
            },
            post2={
                'Host': 'ecard.scuec.edu.cn',
                'Connection': 'keep-alive',
                'Content-Length': '45',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\
                  /537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
                'Referer': 'http://ecard.scuec.edu.cn/accounthisTrjn1.action'
            },
            post3={
                'Host': "ecard.scuec.edu.cn",
                'Referer': "http://ecard.scuec.edu.cn/accounthisTrjn2.action",
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\
                /537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
                'Connection': "keep-alive",
                'Content-Type': "application/x-www-form-urlencoded",
                'Content-Length': "0",
                'cache-control': "no-cache",
            },
            post4={
                'Host': 'ecard.scuec.edu.cn',
                'Connection': 'keep-alive',
                'Content-Length': '55',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit\
                  /537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
                'Referer': 'http://ecard.scuec.edu.cn/accounthisTrjn3.action'
            }
        )
        self.urls = dict(
            account_type_url='http://ecard.scuec.edu.cn/accounthisTrjn.action',
            posturl="http://ecard.scuec.edu.cn/accounthisTrjn{}.action",
            nextpage="http://ecard.scuec.edu.cn/accountconsubBrows.action",
        )
        self.postdata = dict(
            data1={
                'account': '',
                'inputObject': 'all',
                'Submit': '+%C8%B7+%B6%A8+'},
            data2={
                'inputStartDate': '20180903',
                'inputEndDate': '20181229'

            })

    def get_account(self):
        """
        获取账户类型
        :return: 布尔值，指示获取状态
        """
        try:
            account_res = requests.get(url=self.urls['account_type_url'], headers=self.headers['get'],
                                       cookies=self.cookie)
        except requests.exceptions.RequestException:
            return False
        account_res = account_res.content.decode('gb2312')
        tree = etree.HTML(account_res)
        result = tree.xpath('//select[@id="account"]/option/@value')
        if len(result) < 1:
            return False
        else:
            self.postdata['data1']['account'] = result[0]
            return True

    def get_bill(self):
        try:
            postdata1 = parse.urlencode(self.postdata['data1'])
            requests.post(self.urls['posturl'].format('1'),
                          data=postdata1, headers=self.headers['post1'], cookies=self.cookie)
            postdata2 = parse.urlencode(self.postdata['data2'])
            requests.post(self.urls['posturl'].format('2'),
                          data=postdata2, headers=self.headers['post2'], cookies=self.cookie)
            result = requests.post(self.urls['posturl'].format('3'),
                                   headers=self.headers['post3'], cookies=self.cookie)
        except requests.exceptions.RequestException:
            return False
        # 去掉网页中的注释
        re_comment = re.compile('<!--.*-->')
        result_content = re_comment.sub('', result.content.decode('gb2312'))
        tree = etree.HTML(result_content)
        # 抓取页数
        pages_obj = tree.xpath('//*[@id="tables"]/tr[last()]/td/div')
        if len(pages_obj) < 1:
            return False
        pages_regex = re.findall('(?<=共).*?(?=页)', pages_obj[0].text)
        pages = int(pages_regex[0])
        # 抓取所有消费条目并序列化
        all_tr = tree.xpath('//*[@id="tables"]/tr[@class="listbg" or @class="listbg2"]')
        bill = list()
        for tr in all_tr:
            temp = list()
            for td in tr:
                temp.append(td.text)
            bill.append(temp)
        # 获取后续页面内容
        for i in range(pages):
            postdata = self.postdata['data2']
            postdata['pageNum'] = str(i)
            postdata = parse.urlencode(postdata)
            nextpage_res = requests.post(self.urls['nextpage'],
                                         data=postdata, headers=self.headers['post4'], cookies=self.cookie)
            nextpage_content = nextpage_res.content.decode('gb2312')
            nextpage = re_comment.sub('', nextpage_content)
            tree = etree.HTML(nextpage)
            all_tr = tree.xpath('//*[@id="tables"]/tr[@class="listbg" or @class="listbg2"]')
            for tr in all_tr:
                temp = list()
                for td in tr:
                    temp.append(td.text)
                bill.append(temp)
        return bill
