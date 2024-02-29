import sqlite3 #进行SQLite数据库操作

sql = '''
 create table system_movie
 (
 id integer ,
 info_link text,
 pic_link text,
 cname varchar,
 ename varchar,
 score numeric,
 rated numeric,
 introduction text,
 info text,
 movie varchar primary key
 )
 '''  # 创建数据表

conn = sqlite3.connect('test')  # 创建或连接数据库
cursor = conn.cursor()  # 创建游标
'''
    如果不使用游标功能，直接使用select查询，会一次性将结果集打印到屏幕上，你无法针对结果集做第二次编程。
    使用游标功能后，我们可以将得到的结果先保存起来，然后可以随意进行自己的编程，得到我们最终想要的结果集。
'''
cursor.execute(sql)  # 使用游标执行sql命令
conn.commit()  # 提交数据库操作
conn.close()