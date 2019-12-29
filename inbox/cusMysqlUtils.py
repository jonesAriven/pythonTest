#!/usr/bin/python3

import pymysql
import traceback


class MysqlUtils():

    def __init__(self):
        # 打开数据库连接
        self.__db = pymysql.connect("127.0.0.1", "jones", "jones", "test")

    @property
    def db(self):
        return self.__db

    @db.setter
    def db(self, db):
        self.__db = db

    def cus_escape_string(self, sql_param):
        return pymysql(sql_param)

    def insert(self, perfix_sql="", **sql_parma):
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = self.db.cursor()
        try:
            # 执行sql语句
            cursor.execute(perfix_sql)
            # 提交到数据库执行
            self.db.commit()
        except:
            traceback.print_exc()
            # 如果发生错误则回滚
            self.db.rollback()

# db = pymysql.connect("127.0.0.1","jones","jones","test" )
#
# # 使用 cursor() 方法创建一个游标对象 cursor
# cursor = db.cursor()
#
# # 使用 execute()  方法执行 SQL 查询
# cursor.execute("SELECT VERSION()")
#
# # 使用 fetchone() 方法获取单条数据.
# data = cursor.fetchone()
#
# print ("Database version : %s " % data)
#
# # 关闭数据库连接
# db.close()
