# coding: utf-8
"""判断是否是正常访问
    1 区分是人还是爬虫（其他）访问你的网站
    2 是人访问，对他的访问频率进行控制
"""
import tornado.ioloop
import tornado.web

# 设置代理服务器（用来判断是否是爬虫访问）
User_Agent = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0"]
class AcessHandler(tornado.web.RequestHandler):
    async def get(self,*args,**kwargs):
        # 获取请求的代理信息
        ua = self.request.headers["User-Agent"]
        print(ua)
        # 若不是该代理服务器，返回403，禁止访问
        if ua not in User_Agent:
            self.send_error(403)
        else:
            return self.write("hello,welcome my baby!")


"""通过控制台访问，同样报403错误"""
# import urllib.request
# urllib.request.urlopen("http://localhost:8888/")
"""在控制台操作"""

# 控制访问频率(次数+时间)
"""
    1 记录访问者的IP
    2 以IP作为key，访问次数作为值，统计访问记录{key:value}
"""
import time
visit_history = {}
class VisitHandler(tornado.web.RequestHandler):
    def get(self,*args,**kwargs):
        # 获取访问者IP,作为唯一标识
        visit_ip = self.request.remote_ip
        visit_time = time.time()
        if visit_ip not in visit_history:
            # 记录此IP的访问时间，并以列表（可以对时间进行操作，限定时间范围）保存时间，
            visit_history[visit_ip] = [visit_time,]

        # 获取此IP的所有访问记录
        all_counts = visit_history.get(visit_ip)
        self.all_counts = all_counts
        print(all_counts)
        # 删除一分钟前的记录，剩下的就是一分钟内的
        while all_counts and all_counts[-1] < visit_time -60:
            all_counts.pop()

        # 统计一分钟内的访问次数
        print(visit_history)

        if len(all_counts) < 3:
            all_counts.insert(0,visit_time)
        else:
            self.send_error(403)

    def wait(self):
        return None

# 设置路由
def make_app():
    return tornado.web.Application([
        (r'^/$',AcessHandler),
        (r'^/visit/$', VisitHandler),

    ])


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()