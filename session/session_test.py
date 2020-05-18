'''
session对象
它允许我们在不同请求间存储特定用户的信息。
它是在cookies的基础上实现的
并且对cookies进行密钥签名
这意味着用户可以查看你cookies的内容，但是不能修改它，
除非用户知道签名的密钥
'''
#要使用session，我们需要一个密钥，这里介绍session如何工作


from flask import Flask,session,redirect,url_for,escape,request
app = Flask(__name__)

#首页
@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' %escape(session['username'])#escape可以在你模板引擎外做转义
    return 'You are not logged in'

#登录
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''
#登出
@app.route('/logout')
def logout():
    #remove the username from the session if it is there
    session.pop('username',None)
    return redirect(url_for('index'))


#设置并保留这个密钥
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

'''
import os
os.urandom(24)
#'\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
# 把这个值复制粘贴进你的代码中，你就有了密钥

'''

'''
使用基于 cookie 的会话需注意:
 Flask 会将你放进会话对象的值序列化至 Cookies。
 如果你发现某些值在请求之间并没有持久存在，然而确实已经启用了 Cookies，
 但也没有得到明确的错误信息。
 这时，请检查你的页面响应中的 Cookies 的大小，并与 Web 浏览器所支持的大小对比。

'''


if __name__ == '__main__':
    #使服务器公开可用的方法 app.run(host = '0.0.0.0', port = '8080')
    app.run(debug=True)#调试模式，注意设置生产不可用









