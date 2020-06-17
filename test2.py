# coding: utf-8

import tornado.ioloop
import tornado.web


class UploadHandler(tornado.web.RequestHandler):
    """上传文件"""
    async def get(self,*args,**kwargs):
        return self.render("html/upload.html")

    async def post(self,*args,**kwargs):
        """获取请求的文件(images)"""
        # 通过打印知道image的形式：[{'filename': '9b5.jpeg', 'body': b'\d9', 'content_type': 'image/jpeg'}]
        image = self.request.files['img']

        # 遍历image获取数据
        for img in image:
            filename = img.get("filename","")
            body = img.get("body","")
            content_type = img.get("content_type","")

        # 将body存放files中
        import os
        dir = os.path.join(os.getcwd(),"files", filename)
        with open(dir, 'wb') as f:
            f.write(body)

        # 将图片显示到页面
        # 设置响应头，告诉浏览器这是一个图片
        self.set_header("Content-type",content_type)
        # 将图片数据写到页面
        self.write(body)



def make_app():
    return tornado.web.Application([
        (r"^/upload/$", UploadHandler),
    ])

if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()