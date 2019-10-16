import requests
import re
import time
import random
from urllib import parse

class Douban:

    #为了保存cookie
    session = requests.session()

    def login(self,username,password):
        """
        :param username: 豆瓣账户
        :param password:  豆瓣密码
        :return:
        """
        loginUrl = "https://accounts.douban.com/j/mobile/login/basic"
        header = {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded",
                  "Origin": "https://accounts.douban.com",
                  "Referer": "https://accounts.douban.com/passport/login_popup?login_source=anony",
                  "Sec-Fetch-Mode": "cors",
                  "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
                  "X-Requested-With": "XMLHttpRequest"
                  }
        data = {"name": username,
                "password": password,
                "remember": "false",
                "ticket": ""
                }
        try:
            response = self.session.post(loginUrl, headers=header, data=data)
            response.raise_for_status()
        except:
            print("登录失败")

    def search_subject(self,subject):
        """
        :param subject: 搜索关键字
        :return: 如果搜索成功，返回的是对应词条的搜索链接，如活着链接：https://movie.douban.com/subject/1292365/
        """
        subject_encode = parse.urlencode({'q': subject})
        if subject_encode == '':
            print("检索主题不能为null")
            return 1

        url = 'https://www.douban.com/search?source=suggest&%s' % (subject_encode)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()
        except:
            print("搜索失败")
        parttern = '<span>\[电影\]</span>([\s\S]*?)&nbsp;\<a href="https://www.douban.com/link2/\?url=(.+?)&amp;(.+)?(%s[\s,\S]+?)\</a>' % (
            subject)
        results = re.findall(parttern, response.text)
        for result in results:
            for url in result:
                if str(url).startswith('https'):
                    return parse.unquote(url)
        return 1

    def spider_comments(self,url,start,file_path):
        """
         这是爬取一页的影评数据,并将其追加到指定文件中

        :param url:  对应词条的链接
        :param file_path:   文件路径，检索到的影评信息，将会存放在这里
        :return:  检索的影评信息
        """
        comment_url = "%scomments?start=%s&limit=20&sort=new_score&status=P" % (url, start)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
        try:
            response = self.session.get(comment_url, headers=headers)
            response.raise_for_status()
        except:
            print("获取失败")

        comments = re.findall('<span class="short">(.*)</span>', response.text)
        self.write(comments, file_path, response.encoding)
        return len(comments)

    def spider_all_comments(self,url,file_path):
        start = 0
        count = 1
        coments_length = self.spider_comments(url, start, file_path)
        while coments_length != 0:
            start += 20
            print("开始爬第%s页的数据" % (count))
            count += 1
            time.sleep(random.random() * 5)
            coments_length = self.spider_comments(url=url, start=start, file_path=file_path)

    def write(self,comments,file_path,encoding):
        with open(file_path, "a+", encoding=encoding) as file:
            for comment in comments:
                file.write(comment + '\n')

