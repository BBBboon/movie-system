# -*- coding = utf-8 -*-
# @Time : 2022/2/8 16:24
# @Author : Ethan
# @File : get_comment.py
# @Software : PyCharm
import re
import time
import sqlite3
import urllib.request
from bs4 import BeautifulSoup as bs


def main():
    init_db('../db.sqlite3')
    print('数据库连接完成。')
    print("开始获取电影主页超链接。")
    start_url = 'https://movie.douban.com/top250?start='  #要爬取的网址
    total_movie_urls = []
    lose_movies = []

    for i in range(0, 10):
        basic_url = start_url + str(i * 25)  # 切换网页
        basic_content = get_url(basic_url)  # 得到url的网页内容
        print(f"***正在获取第{i+1}页上电影主页超链接...")
        movie_urls = get_movie_url(basic_content)  # 将每页的电影超链接放在一个数组里
        total_movie_urls = total_movie_urls + movie_urls  # 所有电影链接放在一个列表里

    print("所有电影主页超链接获取完毕。")

    i = 0  # 设置计数器
    for movie_url in total_movie_urls:
        i += 1
        print(f"***正在获取第{i}部电影评论信息...")
        movie_comments_information = get_comments(movie_url, i)
        print(movie_comments_information)
        if (movie_comments_information == []):
            for item in range(3):
                print(f"***正在重新获取第{i}部电影评论信息...")
                movie_comments_information = get_comments(movie_url, i)
                print(movie_comments_information)
                time.sleep(1)
                if (movie_comments_information != []):
                    break
                lose_movies.append(i)
        print(f"***正在保存第{i}部电影信息到数据库...")
        save_comments(movie_comments_information, '../db.sqlite3')

    # all_movies_comments = get_comments(total_movie_urls) #得到每部电影所有评论的数组
    # print("所有电影影评获取完毕。")
    # save_comments(all_movies_comments, 'movies_comments.db')
    # print("所有影评信息保存完毕。")



# 得到url的网页内容
def get_url(basic_url):
    headers = {
        "Accept": "text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q = 0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53",
        "Accept - Encoding": "gzip, deflate, br",
        "Accept - Language": "zh - CN, zh;q = 0.9, en;q = 0.8, en - GB;q = 0.7, en - US;q = 0.6",
        "Cookie": 'bid = 4lj - m6PNpCo; gr_user_id = e3de780f - 29e6 - 4f79 - aa37 - a4d559e6e5c8; __gads = ID = bb30e1167c5df01f - 22e55e3ccec800e7: T = 1621742788:RT = 1621742788:S = ALNI_MaTfQcwsSRFFrfiEwFgB2qkR0IYow; viewed = "5333562_4838430_1945005_1929984"; ll = "108289"; _vwo_uuid_v2 = DB99418F6A05C8DECA81714785DA080E0 | 2c3878bc163d6fe427799aa31789152a; __yadk_uid = iZsJvPCK1ovguOgAeGppLYtz4W5P51eW; douban - fav - remind = 1; dbcl2 = "253742241:3G+7T4TxTAU"; push_noty_num = 0; push_doumail_num = 0; __utmv = 30149280.25374; ct = y; Hm_lvt_16a14f3002af32bf3a75dfe352478639 = 1644306515; ap_v = 0, 6.0; ck = KySd; _pk_ref.100001.4cf6 = % 5B % 22 % 22 % 2C % 22 % 22 % 2C1644464800 % 2C % 22https % 3A % 2F % 2Fcn.bing.com % 2F % 22 % 5D; _pk_ses.100001.4cf6 = *; __utma = 30149280.318684309.1621742789.1644461972.1644464800.25; __utmb = 30149280.0.10.1644464800; __utmc = 30149280; __utmz = 30149280.1644464800.25.16.utmcsr = cn.bing.com | utmccn = (referral) | utmcmd = referral | utmcct = /; __utma = 223695111.1113219147.1632023592.1644461972.1644464800.23; __utmb = 223695111.0.10.1644464800; __utmc = 223695111; __utmz = 223695111.1644464800.23.14.utmcsr = cn.bing.com | utmccn = (referral) | utmcmd = referral | utmcct = /; _pk_id.100001.4cf6 = 004ba2103680f441.1632023592.23.1644465078.1644462267.',
        "Referer": "https: // cn.bing.com /"
    }  # 保存头部信息

    request = urllib.request.Request(basic_url,headers=headers) # 对发送的网页头部信息进行模拟，添加头部信息
    try:
        response = urllib.request.urlopen(request)  # 以urlopen方式打开网页
        time.sleep(1)
        basic_content = response.read().decode('utf-8')  # 将网页内容读取为utf-8的格式
    except urllib.error.URLError as e:
        if hasattr(e, "code"):  # hasattr() 函数用于判断对象是否包含对应的属性
            print(e.code)  # 返回错误代码
        if hasattr(e, "reason"):
            print(e.reason)  # 返回错误原因

    return basic_content


# 获取每个电影主页的超链接
def get_movie_url(basic_content):
    soup = bs(basic_content, "html.parser")
    # print(soup)
    movies_urls = []

    all_urls = re.findall(re.compile(r'<a href="(.*?)">'), str(soup))  # 网页中全部的超链接组成一个数组，第11到35个元素是电影链接
    print(all_urls)
    for movie_number in range(0, 25): #1页25部电影
        movies_urls.append(all_urls[11 + movie_number])

    return movies_urls


# 爬取电影影评
def get_comments(movie_url, i):
    punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~“”？，！【】（）、。：；’‘……￥·╮▽￣╭"""  #设置标点字符集
    # all_movies_comments = [] #存储所有电影的影评


    while True:
        try:
            movie_comments_information = []  # 存储一部电影的影评信息

            opened_movie_url = get_url(movie_url)  # 打开电影链接
            time.sleep(1) #睡眠
            basic_comments_url_soup = bs(opened_movie_url, "html.parser")

            movie_name = re.findall(re.compile(r'<span property="v:itemreviewed">(.*?)</span>'), str(basic_comments_url_soup)) #获取电影名
            comments_next_basicurl = re.findall(re.compile(r'<a href="(.*?comments\?)status=P">'), str(basic_comments_url_soup))[0] #获取电影评论翻页的基础网址

            for page in range(0,10): #10页影评
                page_comments_information = []  # 存储一页评论的相关信息

                comments_next_url = comments_next_basicurl + f"start={page*20}&limit=20&status=P&sort=new_score" #影评网址
                opened_comments_url = get_url(comments_next_url) #打开电影的全部影评网页
                time.sleep(1)
                comments_url_soup = bs(opened_comments_url, "html.parser")

                for comment_item in comments_url_soup.find_all("div", class_="comment"): #以每一页上的一个影评模块为单位循环
                    comment_information = [] #存储一个用户评论的相关信息

                    comment_list = re.findall(re.compile(r'<span class="short">(.*?)</span>', re.S),
                                        str(comment_item))  #获取用户评论
                    time.sleep(0.5)
                    if len(comment_list) == 0:
                        comment = ' ' #防止评论为空值
                    else:
                        comment = comment_list[0]
                    comment = re.sub(r'\r|\n|\t', '', comment) #除去字符串中一些无关符号
                    dicts = {i: '' for i in punctuation}
                    punc_table = str.maketrans(dicts)
                    new_comment = comment.translate(punc_table) #除去中英文标点符号
                    new_comment = new_comment.replace(" ","")
                    if len(new_comment) == 0:
                        new_comment = ' '

                    viewer = re.findall(re.compile(r'<a class="" href=".*?">(.*?)</a>'),
                                        str(comment_item)) #获取用户名
                    time.sleep(0.5)

                    star = re.findall(re.compile(r'<span class=".*?" title="(.*?)"></span>'),
                                    str(comment_item)) #获取电影评星
                    time.sleep(0.5)
                    if len(star) == 0:
                        star.append(' ') #防止评星为空值

                    comment_time = re.findall(re.compile(r'<span class="comment-time" title="(.*?)">', re.S), str(comment_item)) #获取评论时间
                    time.sleep(0.5)

                    comment_information = comment_information + movie_name + viewer + star + comment_time
                    comment_information.append(comment)
                    comment_information.append(new_comment)
                    comment_information.append(str(i))
                    print(comment_information)
                    page_comments_information.append(comment_information) #将逐条影评的相关信息存储在数组里
                movie_comments_information= movie_comments_information + page_comments_information #将每个电影的全部影评保存在一个数组里
            break

        except Exception:
            time.sleep(2)

    return movie_comments_information

# 初始化数据库
def init_db(dbpath):
    sql='''
    create table system_mcomments
    (
    id integer primary key autoincrement,
    movie_name varchar,
    viewer_name varchar,
    star varchar,
    comment_time datetime,
    comment text,
    new_comment text, 
    movie_id integer,
    foreign key (movie_id) references system_movieinfo(id)
    )
    ''' #创建数据表

    conn = sqlite3.connect(dbpath) #创建或链接数据库
    cursor = conn.cursor() #创建游标
    cursor.execute(sql) #使用游标执行sql命令
    conn.commit() #提交数据库操作

    cursor.close()
    conn.close()

# 将爬取的影评保存在数据库中
def save_comments(movie_comments_information, dbpath):
    conn = sqlite3.connect(dbpath) #创建或链接数据库
    cursor = conn.cursor() #创建游标

    for comment_information in movie_comments_information:
        for index in range(len(comment_information)):
            if index == 1:
                comment_information[1] = comment_information[1].replace('"','')
            if index == 6:
                continue #整型不加双引号
            comment_information[index] = '"' + comment_information[index] + '"'

        sql = '''
        insert into system_mcomments(
        movie_name, viewer_name, star, comment_time, comment, new_comment, movie_id
        )
        values(%s);'''%",".join(comment_information)

        print(sql)

        cursor.execute(sql)
        conn.commit()

    cursor.close()
    conn.close()






if __name__ == "__main__":
    main()
