# -*- coding = utf-8 -*-
# @Time : 2021/11/12 11:21
# @Author : Ethan
# @File : spider.py
# @Software : PyCharm

import time
from bs4 import BeautifulSoup #网页解析，获取数据
import re #正则表达式，进行文字匹配
import urllib.request,urllib.error #指定url，获取网页数据
import xlwt #进行excel操作
import sqlite3 #进行SQLite数据库操作

# 先定义函数，再用main()函数
def main():
    baseurl = "https://movie.douban.com/top250?start="
    datalist = getData(baseurl)

    # savepath = "doubanmovieTop250.xls"
    # saveData(datalist, savepath)

    print('开始保存数据...')
    dbpath = '../db.sqlite3'
    saveData2DB(datalist, dbpath)

# 影片详情链接的规则
findLink = re.compile(r'<a href="(.*?)">') #创建正则表达式，表示规则（字符串的模式）
# 影片图片的规则
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S) #re.S让换行符包含在字符中
# 影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
# 影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 电影的经典一句话
findInq = re.compile(r'<span class="inq">(.*?)</span>')
# 影片概况
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)
# 影片内容介绍
# find_intro = re.compile(r'<span class="all hidden">(.*?)</span>', flags=re.S)
# 电影名（外键）
find_name = re.compile(r'<span property="v:itemreviewed">(.*?)</span>')
# 爬取网页
def getData(baseurl):
    datalist = []
    counter = 0 #设置计数器

    for i in range(0,10): #调用获取页面信息的函数10次
        url = baseurl + str(i*25)
        # datalist = askURL(url) #保存获取到的网页源码
        html = askURL(url)  # 保存获取到的网页源码
        # print(askURL(url))

        # 逐一解析数据
        soup = BeautifulSoup(html,"html.parser") #soup=beautifulsoup(解析内容,解析器)
        # 查找符合要求的字符串，形成列表；class后面的_表示class属性
        for item in soup.find_all("div",class_="item"): #循环25部电影
            data = []
            item = str(item)

            # 影片编号
            counter = counter + 1
            data.append(str(counter))

            # 影片详情的链接
            link = re.findall(findLink,item)[0] #加索引可以避免以数组形式输出
            data.append(link) #添加链接在列表中

            imgSrc = re.findall(findImgSrc,item)[0]
            data.append(imgSrc)

            titles = re.findall(findTitle,item) #片名可能有多个
            if(len(titles)==2):
                data.append(titles[0]) #添加中文名
                temp = titles[1].replace("/","") #去掉无关符号
                data.append(temp.strip()) #添加外国名
            else:
                data.append(titles[0]) #只有中文名
                data.append(' ') #留空，保存到excel表里防止不能对齐

            rating = re.findall(findRating,item)[0]
            data.append(rating) #添加评分

            judgeNum = re.findall(findJudge,item)[0]
            data.append(judgeNum) #添加评价人数

            inq_string = re.findall(findInq,item)
            if len(inq_string) != 0:
                data.append(inq_string[0]) #添加经典一句话
                inq = inq_string[0].replace("。","") #去掉句号
                data.append(inq) #添加处理后的经典一句话
            else:
                data.append(" ") #留空
                data.append(' ')

            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd) #去掉<br/>
            bd = re.sub('/'," ",bd) #去掉/
            data.append(bd.strip()) #去掉前后的空格

            # 进入电影主页爬取想要的内容
            movie_html = askURL(link)
            time.sleep(3)
            movie_soup = BeautifulSoup(movie_html, 'html.parser')
            # movie_intro = re.findall(find_intro, str(movie_soup)) #获取电影简介
            name = re.findall(find_name, str(movie_soup))[0] #获取电影名（外键）
            data.append(name)

            # movie_info = re.findall(re.compile(r'<div id="info">(.*?)</div>'), str(movie_soup)) #获取电影信息
            # print(movie_info)
            # movie_source = re.findall(re.compile(r'<ul class="bs">(.*?)</ul>'), str(movie_soup)) #获取电影资源
            # print(movie_source)

            print(data)
            datalist.append(data) #将处理好的一部电影信息放入datalist


    return datalist

# 得到指定一个URL的网页内容
def askURL(url):
    # 模拟浏览器头部信息向服务器发送消息
    # 用户代理表示告诉服务器我们是什么型号的机器、浏览器（本质是告诉浏览器我们可以接受什么样水平的文件内容）
    headers = {
        "Accept": "text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q = 0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53",
        "Accept - Encoding": "gzip, deflate, br",
        "Accept - Language": "zh - CN, zh;q = 0.9, en;q = 0.8, en - GB;q = 0.7, en - US;q = 0.6",
        "Cookie": 'bid = 4lj - m6PNpCo; gr_user_id = e3de780f - 29e6 - 4f79 - aa37 - a4d559e6e5c8; __gads = ID = bb30e1167c5df01f - 22e55e3ccec800e7: T = 1621742788:RT = 1621742788:S = ALNI_MaTfQcwsSRFFrfiEwFgB2qkR0IYow; viewed = "5333562_4838430_1945005_1929984"; ll = "108289"; _vwo_uuid_v2 = DB99418F6A05C8DECA81714785DA080E0 | 2c3878bc163d6fe427799aa31789152a; __yadk_uid = iZsJvPCK1ovguOgAeGppLYtz4W5P51eW; douban - fav - remind = 1; dbcl2 = "253742241:3G+7T4TxTAU"; push_noty_num = 0; push_doumail_num = 0; __utmv = 30149280.25374; ct = y; Hm_lvt_16a14f3002af32bf3a75dfe352478639 = 1644306515; ap_v = 0, 6.0; ck = KySd; _pk_ref.100001.4cf6 = % 5B % 22 % 22 % 2C % 22 % 22 % 2C1644464800 % 2C % 22https % 3A % 2F % 2Fcn.bing.com % 2F % 22 % 5D; _pk_ses.100001.4cf6 = *; __utma = 30149280.318684309.1621742789.1644461972.1644464800.25; __utmb = 30149280.0.10.1644464800; __utmc = 30149280; __utmz = 30149280.1644464800.25.16.utmcsr = cn.bing.com | utmccn = (referral) | utmcmd = referral | utmcct = /; __utma = 223695111.1113219147.1632023592.1644461972.1644464800.23; __utmb = 223695111.0.10.1644464800; __utmc = 223695111; __utmz = 223695111.1644464800.23.14.utmcsr = cn.bing.com | utmccn = (referral) | utmcmd = referral | utmcct = /; _pk_id.100001.4cf6 = 004ba2103680f441.1632023592.23.1644465078.1644462267.',
        "Referer": "https: // cn.bing.com /"
    }  # 保存头部信息

    request = urllib.request.Request(url,headers=headers) #对 headers（网页头信息）进行模拟，添加头部信息
    time.sleep(1)
    try:
        response = urllib.request.urlopen(request) #urlopen方式打开网址
        html = response.read().decode("utf-8")
        # print(html)
        #print(type(html))
    except urllib.error.URLError as e:
        if hasattr(e,"reason"): #hasattr() 函数用于判断对象是否包含对应的属性
            print(e.reason) #返回错误原因

    return html


#保存数据
def saveData(datalist, savepath):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0) #创建workbook对象，style_compression:表示是否压缩
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True) #创建工作表，cell_overwrite_ok:表示是否可以覆盖单元格
    column = ('电影详情链接', '图片链接', '影片中文名', '影片外国名', '评分', '评价数', '概况', '相关信息')

    for column_number in range(0,8):
        sheet.write(0, column_number, column[column_number]) #放入列名

    for movie_number in range(0,250):
        print(f"第{movie_number+1}条")
        data = datalist[movie_number]
        for item in range(0,8):
            sheet.write(movie_number+1, item, data[item]) #放入数据

    book.save(savepath)

def saveData2DB(datalist, dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            if index == 0 or index == 5 or index == 6:
                continue
            data[index] = '"' + data[index] + '"' #给每个元素加上""
        sql = '''
        insert into system_movie(
        id, info_link, pic_link, cname, ename, score, rated, introduction, new_introduction, info, movie
        )
        values(%s);'''%",".join(data) #%s是占位符，后面的join方法意思是将数组中的每个元素提取出来并都用,分隔，然后合成一个新字符串
        print(sql)

        cur.execute(sql)
        conn.commit()

    cur.close()
    conn.close()



def init_db(dbpath):

    sql = '''
    create table system_movie
    (
    id integer,
    info_link text,
    pic_link text,
    cname varchar,
    ename varchar,
    score numeric,
    rated numeric,
    introduction text,
    new_introduction text,
    info text,
    movie varchar primary key
    )
    ''' #创建数据表

    conn = sqlite3.connect(dbpath) #创建或连接数据库
    cursor = conn.cursor() #创建游标
    '''
        如果不使用游标功能，直接使用select查询，会一次性将结果集打印到屏幕上，你无法针对结果集做第二次编程。
        使用游标功能后，我们可以将得到的结果先保存起来，然后可以随意进行自己的编程，得到我们最终想要的结果集。
    '''
    cursor.execute(sql) #使用游标执行sql命令
    conn.commit() #提交数据库操作
    conn.close()

if __name__ == "__main__": #当程序执行时的入口
    #调用函数
    main()



