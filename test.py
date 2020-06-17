# coding: utf-8
import tornado.ioloop
import tornado.web


"""
IO复用模式:select,poll,epoll
window/Mac:select -不断轮询每个socket对象，效率较低
linus:epoll -第一次轮询每个socket对象，同时绑定一个回调函数，
             以后根据回调函数返回的状态（休眠/运行..)判断是否调用这个socket对象
"""
# 创建处理类
class IndexHandler(tornado.web.RequestHandler):
    """相当于django里的视图类"""
    async def get(self, *args, **kwargs):
        # uname = self.get_argument("uname")
        # pwd = self.get_argument("pwd")
        return self.render("html/login.html")


class LoginHandler(tornado.web.RequestHandler):
    """登录页"""
    async def get(self, *args, **kwargs):
        uname = self.get_argument("uname")
        pwd = self.get_argument("pwd")
        print(uname, pwd)
        return self.write("%s \n %s" % (uname, pwd))

    async def post(self, *args, **kwargs):
        uname = self.get_argument("uname")
        pwd = self.get_argument("pwd")
        print("####################")
        self.write("welcome %s, you have logged in the site" % uname)

# 定义方法，创建Application对象，相当于路由
def make_app():
    return tornado.web.Application([
        (r"^/$", IndexHandler),
        (r"^/login/$", LoginHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
