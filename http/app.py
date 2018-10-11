# -*- coding:utf-8 -*-
from flask import Flask, abort

app = Flask(__name__)  # 创建对象


@app.route("/")  # 定义一个路由，指定一个路由
def index():  # 路由指向index
    return "<h1 style='color:red'>hello world</h1>"

#指定不同状态码 F12 network 查看status
@app.route("/h203")
def h203():
    return "<h1 style='color:blue'>203</h1>", 203

#附加或修改首部字段 手动重定向 F12 点击h303
@app.route("/h303")
def h303():
    return "", 303, {'Location':'http://www.holydatura.com'}


#redirect重定向
@app.route("/h303")
def h303():
    return "", 303, {'Location':'http://www.holydatura.com'}

@app.route('/404')
def not_found():
    abort(404)


if __name__ == "__main__":  # 运行程序
    app.run()  # 整理代码格式--菜单code->reformat code
