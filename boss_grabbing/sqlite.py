import sqlite3
import time

con = sqlite3.connect('sqlite3.db')
cur = con.cursor()
print("sqlite连接成功")


class Sqlite(object):
    # 检查公司是否存在
    @classmethod
    def select_db(cls, company_id):
        sql = 'select count(1) from company where id=?'
        return cur.execute(sql, (company_id,)).fetchall()

    @classmethod
    def insert_db(cls, item):
        values = (
            item['url'],
            item['name'],
            item['area'],
            item['finance'],
            item['size'],
            item['description'],
            item['addresses'],
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        )

        sql = 'INSERT INTO company (id,name,area,finance,size,DESCRIPTION,ADDRESS,CREATE_TIME) VALUES(?,?,?,?,?,?,?,?)'
        cur.execute(sql, values)
        con.commit()