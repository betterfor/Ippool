import pymysql

class DBHelper:
    # 构造函数
    def __init__(self):
        try:
            config = {
                'host':'127.0.0.1',
                'user':'root',
                'password':'xj',
                'db':'proxy',
                'port':3306,
                'charset':'utf8'
            }
            self.conn = pymysql.connect(**config)
            self.cursor = self.conn.cursor()
            print('连接数据库')
        except Exception as e:
            print('连接错误',e)

    # 关闭数据库
    def __del__(self):
        self.conn.close()
        print('关闭数据库')

    # 执行数据库的sql语句，插入
    def insertDB(self,protocol,ip,port):
        print("正在插入",protocol,ip,port)
        try:
            sql = "insert into proxy(protocol,ip,port) values ('%s','%s','%s')"
            self.cursor.execute(sql % (protocol,ip,port))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("insert error",e)

    # 删除一条记录
    def deleteDB(self,id):
        try:
            sql="delete from proxy where id = '%s'"
            self.cursor.execute(sql,id)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("删除失败",e)

    # 查询第一条数据
    def queryDB(self):
        sql = "select * from proxy"
        self.cursor.execute(sql)
        # 获取第一行
        row = self.cursor.fetchone()
        return row

    def queryAll(self):
        sql = "select * from proxy"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

# if __name__=='__main__':
#     dbhelper = DBHelper()
#     dbhelper.insertDB('http' ,'119.101.115.89' ,'9999')
#     dbhelper.deleteDB(6)
#     print(dbhelper.queryDB()[0])