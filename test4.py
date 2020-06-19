# coding: utf-8
import tornado.web
import tornado.ioloop
import pymysql


db = pymysql.connect(host="127.0.0.1",port=33060,user="root",password="HYKD1412KID.xuxiancheng",database="tornado")
cursor = db.cursor()
# datas = cursor.execute("select version();")
# print(datas)
# db.close()

class RegisterHandler(tornado.web.RequestHandler):
    """用户注册"""
    def get(self,*args,**kwargs):
        # 获取注册页面
        return self.render("html/register.html")


    def post(self, *args, **kwargs):
        # 获取数据
        uname = self.get_argument("uname")
        pwd = self.get_argument("pwd")
        print(uname,pwd)
        # 将数据插入数据库并保存
        try:
            sql = "insert into register values ('%s','%s')" % (uname,pwd)
            cursor.execute(sql)
            db.commit()
            self.write("数据保存成功")
        except:
            db.rollback()
            self.redirect("/register/")


"""用户注册时，生成token作为用户标识返回给用户，每次访问后，根据时间更新token"""
import hashlib
import datetime
def md5(user):
    ctime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    m = hashlib.md5(bytes(user,encoding="utf-8"))
    m.update(bytes(ctime,encoding="utf-8"))
    return m.hexdigest()

"""common utils"""


def make_app():
    """设置路由"""
    return tornado.web.Application([
        (r'^/register/$', RegisterHandler)
    ])


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()