# -*- coding: utf-8 -*-
import re
from time import sleep
import requests
from bs4 import BeautifulSoup as bs


class NianDu:
    @staticmethod
    def login(username, password):
        session = requests.Session()
        start_url = "http://id.scuec.edu.cn/authserver/login?service=http%3A%2F%2Fehall.scuec.edu.cn%2Flogin%3Fservice%3Dhttp%3A%2F%2Fehall.scuec.edu.cn%2Fnew%2Findex.html"
        headers = dict(
            headers1={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Host': 'id.scuec.edu.cn',
                'Pragma': 'no-cache',
                'Referer': 'http://ehall.scuec.edu.cn/new/index.html',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
            },
            headers2={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Content-Length': '175',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'id.scuec.edu.cn',
                'Origin': 'http://id.scuec.edu.cn',
                'Pragma': 'no-cache',
                'Referer': start_url,
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
            }
        )
        try:
            start_repo = session.get(start_url, headers=headers['headers1'])
            soup = bs(start_repo.text, 'html.parser')
            lt = soup.find_all(name='input', attrs={'name': 'lt'})[0].get("value")
            dllt = soup.find_all(name='input', attrs={'name': 'dllt'})[0].get("value")
            execution = soup.find_all(name='input', attrs={'name': 'execution'})[0].get("value")
            _eventId = soup.find_all(name='input', attrs={'name': '_eventId'})[0].get("value")
            rmShown = soup.find_all(name='input', attrs={'name': 'rmShown'})[0].get("value")
        except Exception as e:
            # 请求登录首页失败
            return "error_1"

        for item in session.cookies:
            if item.name == "JSESSIONID_AUTH":
                auth = "JESSESIONID_AUTH=" + str(item.value)

        headers['headers2']['Cookie'] = start_repo.headers['Set-Cookie']
        postUrl = "http://id.scuec.edu.cn/authserver/login;" + auth + "?service=http%3A%2F%2Fehall.scuec.edu.cn%2Flogin%3Fservice%3Dhttp%3A%2F%2Fehall.scuec.edu.cn%2Fnew%2Findex.html"
        postData = {
            'username': username,
            'password': password,
            'lt': lt,
            'dllt': dllt,
            'execution': execution,
            '_eventId': _eventId,
            'rmShown': rmShown
        }

        try:
            post_resp = session.post(postUrl, postData, headers['headers2'], allow_redirects=False)
            post_resp.encoding = "utf-8"
            # print(post_resp.text)
            if "您提供的用户名或者密码有误" in post_resp.text:
                return "error_2"
        except Exception as e:
            return "error_3"
        sleep(5)

        headers = dict(
            jw1={
                'Host': 'id.scuec.edu.cn',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Referer': 'http://ehall.scuec.edu.cn/new/index.html',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
            },
            jw2={
                'Host': 'ssfw.scuec.edu.cn',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Referer': 'http://ehall.scuec.edu.cn/new/index.html',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
            }
        )
        jwUrl1 = "http://id.scuec.edu.cn/authserver/login?service=http://ssfw.scuec.edu.cn/ssfw/j_spring_ids_security_check"
        jwxtUrl = "http://ssfw.scuec.edu.cn/ssfw/index.do"

        # 获取cookie
        try:
            jw_res1 = session.get(jwUrl1, headers=headers['jw1'], allow_redirects=False)
            jwUrl2 = jw_res1.headers['Location']
            jw_res2 = session.get(jwUrl2, headers=headers['jw2'], allow_redirects=False)
            headers['jw2']['Cookie'] = jw_res2.headers['Set-Cookie']
            rrrr = session.get("http://ssfw.scuec.edu.cn/ssfw/j_spring_ids_security_check", headers=headers['jw2'],
                               allow_redirects=False)
            headers['jw2']['Cookie'] = jw_res2.headers['Set-Cookie']
            jwRes = session.get(jwxtUrl, headers=headers['jw2'])
        except Exception as e1:
            # 请求教务系统失败
            return "error_3"
        return session

    @staticmethod
    def number(session):
        jw3 = {
            # 'Referer': 'http://ehall.scuec.edu.cn/new/index.html',
            'Cache-Control': 'no-cache',
            'Host': 'ssfw.scuec.edu.cn',
            'Proxy-Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Referer': 'http://ssfw.scuec.edu.cn/ssfw/xkgl/xkjgcx.do',
            'Referer': 'http://ssfw.scuec.edu.cn/ssfw/index.do',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        xinxi = "http://ssfw.scuec.edu.cn/ssfw/xjgl/jbxx.do"
        try:
            xRes = session.get(xinxi, headers=jw3)
            # print(xRes.text)
        except Exception as e:
            return "error_4"
        # return xRes.text

        try:
            soup = bs(xRes.text, 'html.parser')
            name = soup.find('input', {'id': 'xm'})['value']
            number = soup.find('input', {'id': 'zjh'})['value']
            # wel=soup.find('div',{'class':'welMessage'})
            yxdm = soup.find('input', id='yxdm')['value']

            password = number[11:17]
            # local = re.findall("【(.*)】", str(wel))
            # xueyuanLocal=[str(i) for i in local]
            # xueyuan="".join(xueyuanLocal)
            url = "http://ssfw.scuec.edu.cn/ssfw/selectrange.widgets"
            headers = {
                'Accept': 'application / json, text / javascript, * / *; q = 0.01',
                'Accept - Encoding': 'gzip, deflate',
                'Accept - Language': 'zh - CN, zh;q = 0.9',
                'Cache - Control': 'no - cache',
                'Connection': 'keep - alive',
                'Content - Length': '526',
                'Content - Type': 'application / x - www - form - urlencoded;charset = UTF - 8',
                'Host': 'ssfw.scuec.edu.cn',
                'Origin': 'http: // ssfw.scuec.edu.cn',
                'Pragma': 'no - cache',
                'Referer': 'http: // ssfw.scuec.edu.cn / ssfw / xjgl / jbxx.do',
                'User - Agent': 'Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 70.0.3538.67Safari / 537.36',
                'X - Requested - With': 'XMLHttpRequest'
            }

            postData = {
                'baseTypes': 'dwdm',
                'values': yxdm,
                'keys': '7',
            }

            res_xueyuan = session.post(url, headers=headers, data=postData)
            str_res = res_xueyuan.text[1:-1]
            xueyuan = eval(str_res)['label']
        except Exception as e:
            return "error_5"
        return name, password, xueyuan

    @staticmethod
    def kebiao(session, username):
        kbUrl = "http://ssfw.scuec.edu.cn/ssfw/pkgl/kcbxx/4/2018-2019-1.do?flag=4&xnxqdm=2018-2019-1"
        jw3 = {
            # 'Referer': 'http://ehall.scuec.edu.cn/new/index.html',
            'Cache-Control': 'no-cache',
            'Host': 'ssfw.scuec.edu.cn',
            'Proxy-Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Referer': 'http://ssfw.scuec.edu.cn/ssfw/xkgl/xkjgcx.do',
            'Referer': 'http://ssfw.scuec.edu.cn/ssfw/index.do',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        try:
            kRes = session.get(kbUrl, headers=jw3)
            # print(kRes.text)
        except Exception as e:
            return "error_6"
        # return kRes.text
        # username="201621091077"
        year = username[0:4]
        term = (2018 - int(year)) * 2 + 1
        # print(term)
        try:
            soup = bs(kRes.text, 'html.parser')
            # 课程，周数，节数
            step1 = []
            # 课程
            step2 = []
            kebiao1 = soup.findAll('td', {'rowspan': '2'})
            kebiao2 = soup.findAll('td', {'rowspan': '3'})
            kebiao3 = soup.findAll('td', {'rowspan': '4'})
            for child in kebiao2:
                kebiao1.append(child)
            for child in kebiao3:
                kebiao1.append((child))
            # print(kebiao1)

            # 考虑老师在教务系统修改课的情况
            for i in kebiao1:
                if "<img" in str(i):
                    local = re.findall(r"</div>(.*)<img", str(i))
                else:
                    if "<br/>" in str(i):
                        local = re.findall(r"</div>(.*)<br/>", str(i))
                    else:
                        local = re.findall(r"</div>(.*)<br>", str(i))
                step1.append(local[0])

            # 考虑一个td里面有多个课程的情况
            for i in step1:
                if "<hr/>" in str(i):
                    x = str(i).split("<hr/>")[0]
                    y = "</div>\xa0" + str(i).split("<hr/>")[1]
                    step2.append(x)
                    step2.append(y)
                else:
                    step2.append(i)

            dic = {}
            for i in step2:
                num = re.findall('\d+', str(i))

                course = re.findall(r"</div>\xa0(.*)]", str(i))
                # print(course)
                nums = re.findall('\d+', str(course))
                # print(len(nums))
                if len(nums) == 1:
                    num1 = int(num[1])
                    num2 = int(num[2])
                    num3 = int(num[3])
                    num4 = int(num[4])
                elif len(nums) == 2:
                    num1 = int(num[2])
                    num2 = int(num[3])
                    num3 = int(num[4])
                    num4 = int(num[5])
                elif len(nums) == 3:
                    num1 = int(num[3])
                    num2 = int(num[4])
                    num3 = int(num[5])
                    num4 = int(num[6])

                if "周(单)" in str(i):
                    weekCount1 = 0
                    for k in range(num1, num2 + 1):
                        if (k % 2 != 0):
                            weekCount1 = weekCount1 + 1
                    classCount = weekCount1 * (num4 - num3 + 1)
                elif "周(双)" in str(i):
                    weekCount2 = 0
                    for k in range(num1, num2 + 1):
                        if (k % 2 != 0):
                            weekCount2 = weekCount2 + 1
                    classCount = weekCount2 * (num4 - num3 + 1)
                else:
                    classCount = (num2 - num1 + 1) * (num4 - num3 + 1)
                # print(classCount)
                if not str(course) in dic:
                    dic[str(course)] = classCount
                else:
                    dic[str(course)] = dic[str(course)] + classCount
            # print(dic)
            courseCount = len(dic)
            # print(courseCount)
            classCount = 0
            max_value = 0
            for name, value in dic.items():
                if value > max_value:
                    max_value = value
                    courseName = name
                classCount += value
            # print(classCount)
            classDay = round(classCount * 3 / 4 / 24)
            # print(classDay)
            # print(max_value)
            list1 = courseName
            list2 = list1[2:len(list1) - 2]
            list3 = list2 + "]"
            # print(term,courseCount,classCount,classDay,list3)
        except Exception as e3:
            return "error_6"
        return term, courseCount, classCount, classDay, list3
