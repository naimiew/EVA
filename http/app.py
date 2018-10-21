# -*- coding:utf-8 -*-
from flask import *
import os

try:
    from urlparse import urlparse, urljoin
except ImportError:  # 兼容python3
    from urllib.parse import urlparse, urljoin
from jinja2 import escape
from jinja2.utils import generate_lorem_ipsum
from flask import Flask, make_response, request, redirect, url_for, abort, session, jsonify
# Flask, abort, redirect, url_for

app = Flask(__name__)  # 创建对象
app.secret_key = os.getenv('SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'  # session 解决报错问题1


@app.route("/")  # 定义一个路由，指定一个路由
def index():  # 路由指向index
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'May i help you?')
    response = '<h1>Hello. %s</h1>' % escape(name)  # + ' *** ' + os.getenv('SECRET_KEY') + ' *** ')
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
def justlogin():
    session['logged_in'] = True
    return redirect(url_for('index'))


# protect view
@app.route('/justadmin')
def justadmin():
    if 'logged_in' not in session:
        return redirect(url_for('h203'))
    return 'Welcome to admin page.'


# log out user
@app.route('/justlogout')
def justlogout():
    if 'logged_in' in session:
        session.pop('logged_in')  # 清除session
        resp = make_response(redirect(url_for('index')))
        resp.delete_cookie('name')  # 清除cookie
        return resp


# AJAX
@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)
    return '''
<h1>A very long post</h1>
<div class="body">%s</div>
<button id="load">Load More</button>
<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<script type="text/javascript">
$(function() {
    $('#load').click(function() {
        $.ajax({
            url: '/more',  
            type: 'get',
            success: function(data){
                $('.body').append(data);
            }
        })
    })
})
</script>''' % post_body


@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n=1)

# redirect to last page  跟着写的 http进阶
@app.route('/hfoo')
def hfoo():
    return '<h1>Foo page</h1><a href="%s">Do something and redirect</a>' \
           % url_for('do_something', next=request.full_path)


@app.route('/hbar')
def hbar():
    return '<h1>Bar page</h1><a href="%s">Do something and redirect</a>' \
           % url_for('do_something', next=request.full_path)


@app.route('/do-something')
def do_something():
    # do something here
    return redirect_back()


def is_safe_url(target):
    ref_url = urlparse(request.host_url)  # 获取主机url
    test_url = urlparse(urljoin(request.host_url, target))  # 目标url转绝对url
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


# 重定向回上一页  书里 40%的位置 url_for() 多余的关键字参数会被作为查询字符串附加到生成的URL后面
def redirect_back(default='hh', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


if __name__ == "__main__":  # 运行程序
    app.debug = True  # session 解决报错问题2
    app.run()
