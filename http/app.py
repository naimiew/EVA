# -*- coding:utf-8 -*-
from flask import *

# Flask, abort, redirect, url_for

app = Flask(__name__)  # 创建对象


@app.route("/")  # 定义一个路由，指定一个路由
def index():  # 路由指向index
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'May i help you?')
    response = '<h1>Hello, %s</h1>' % escape(name)
    if 'logged_in' in session:
        response += '[Authenticated]'
    else:
        response += '[Not Authenticated]'
    return response
    # return "<h1 style='color:red'>hello world</h1>"


# 指定不同状态码 F12 network 查看status
@app.route("/h203")
def h203():
    return "<h1 style='color:blue'>203</h1>", 203


# 附加或修改首部字段 手动重定向 F12 点击h303
@app.route("/h303")
def h303():
    return "", 303, {'Location': 'http://www.holydatura.com'}


# redirect重定向 手动重定向 F12 点击hredirect 查看status 302
@app.route("/hredirect")
def hredirect():
    return redirect('http://www.holydatura.com')


# redirect-url_for  一定不要加/  这是个惨案
@app.route("/hh")
def hh():
    return redirect(url_for('hi'))


@app.route("/hi")
def hi():
    return "<h1 style='color:yellow'>hi</h1>"


# 手动返回404   页面就是提示Not Found
@app.route('/404')
def not_found():
    abort(404)


# mimetype MIME类型
# 纯文本'text/plain' HTML'text/html' XML'application/xml' JSON’application/json‘
@app.route('/hmime', defaults={'content_type': 'text'})  # 默认值
@app.route('/hmime/<content_type>')
def hmime(content_type):
    content_type = content_type.lower()  # lower() 方法转换字符串中所有大写字符为小写。
    if content_type == 'text':
        body = '''
                Note
                to: Peter
                from: Jane
                heading: Reminder
                body: Don't forget the party!
               '''
        response = make_response(body)
        response.mimetype = 'text/plain'
        return response

    elif content_type == 'html':
        body = '''
                <!DOCTYPE html>
                    <html>
                    <head></head>
                    <body>
                      <h1>Note</h1>
                      <p>to: Peter</p>
                      <p>from: Jane</p>
                      <p>heading: Reminder</p>
                      <p>body: <strong>Don't forget the party!</strong></p>
                    </body>
                    </html>
               '''
        response = make_response(body)
        response.mimetype = 'text/html'
        return response

    elif content_type == 'xml':
        # xml格式要求别开头加tab
        body = '''<?xml version="1.0" encoding="UTF-8"?>
                    <note>
                      <to>Peter</to>
                      <from>Jane</from>
                      <heading>Reminder</heading>
                      <body>Don't forget the party!</body>
                    </note>
               '''
        response = make_response(body)
        response.mimetype = 'application/xml'
        return response

    elif content_type == 'json':
        body = {
            "note": {
                "to": "Peter",
                "from": "Jane",
                "heading": "Remider",
                "body": "Don't forget the party!"
            }
        }
        # JSON 不能这样response
        # response = make_response(body)  应该dumps()方法  字典，列表，元组  一般不这样
        # 优化为 jsonify
        response = make_response(json.dumps(body))
        response.mimetype = 'application/json'
        return response

    elif content_type == 'error':
        return jsonify(message='ERROR!'), 500

    elif content_type == 'jsonify':
        body = {
            "note": {
                "to": "Peter",
                "from": "Jane",
                "heading": "Remider",
                "body": "Don't forget the party!"
            }
        }
        response = jsonify(body)

    else:
        return redirect(url_for('not_found'))  # 重定向404
    return response  # 返回jsonify(body)


# cookie
# set
@app.route('/mycookie/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('index')))
    response.set_cookie('name', name)
    return response


# log in user
@app.route('/justlogin')
def login():
    session['logged_in'] = True
    return redirect(url_for('index'))


# protect view
@app.route('/justadmin')
def admin():
    if 'logged_in' not in session:
        return redirect(url_for('h203'))
    return 'Welcome to admin page.'


# log out user
@app.route('/justlogout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')  # 清除
    return redirect(url_for('index'))


# 卡在python-dotenv 的.env 与 session

if __name__ == "__main__":  # 运行程序
    app.run()
