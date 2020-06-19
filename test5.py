# coding: utf-8

"""重定向，路由逆向访问"""
#     client:                  server:
# 1       request1(url)   -->
# 2                <--   response1(304:重定向&new url)
# 3     request2(new url) -->
# 4                <--   response2(right html)

import tornado.web
import tornado.ioloop
from tornado.web import RedirectHandler
from tornado.routing import URLSpec

"""实现：输入我定义的URL，直接访问百度
    1.通过浏览器的控制台可以看到，返回的是302临时重定向状态码
    2.设置响应码（3开头），设置响应url
    3.自带模块：from tornado.web import RedirectHandler
       在路由中设置重定向url
    4.逆向访问；from tornado.routing import URLSpec
    原理：通过一个url找到重定向的url，
"""
class IndexHandler(tornado.web.RequestHandler):
    def get(self,*args,**kwargs):
        # 1.
        # 默认302重定向，可在源码查看
        # self.redirect("https://www.baidu.com")

        # 2.
        self.set_status(302)
        self.set_header('Location',"https://www.jd.com")

class ReverseHandler(tornado.web.RequestHandler):
    """逆向查询"""
    def get(self,*args,**kwargs):
        self.redirect(self.reverse_url("hahaha"))

def make_app():
    return tornado.web.Application([
        (r'^/$',IndexHandler),

        # 3.系统自带重定向
        (r'^/red/$', RedirectHandler,{"url":"https://www.baidu.com"}),

        # 通过name="hahaha"找到 IndexHandler视图类
        URLSpec(r'^/dfhfdgsjdfvbjhdbvdfnb/$', IndexHandler,name="hahaha"),
        # 设置逆向路由的视图类
        (r'^/reverse/$', ReverseHandler),
    ])

if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

