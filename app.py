from flask import Flask,request,render_template,make_response,redirect,url_for,abort,current_app#可以是import进来一个函数 也可以直接*
import json
from werkzeug.utils import secure_filename
#哈哈，不错，保存一下有热更新,虚拟环境env_flask
#还有一点pre

# "import dir 目录下的 b.py 文件"
# import dir.b

'''
1.第一个参数是应用模块或者包的名称。 
如果你使用单一的模块（如本例），你应该使用 __name__ ，
因为模块的名称将会因其作为单独应用启动还是作为模块导入而有不同
自己启动的时候，实际的模块名就是__main__,在其他部分作为模块导入的时候，就以实际的导入名为主
这是必须的，这样 Flask 才知道到哪去找模板、静态文件等等。详情见 Flask 的文档。
'''
app = Flask(__name__)


'''2.用route装饰器告诉Flask什么样的URL能触发我们的函数'''

@app.route('/')
def index():
    return 'index Page'


'''3.给url添加变量内容，还可以指定类型'''

@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id


'''4.唯一URL/重定向行为'''
#有/的话，不输会自动补全，没/的话不输会报404，路径没找到
@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

'''5.url_for构造url，这个见url_for_test.py'''


'''6.http方法'''
#默认是GET但可以指定
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        return '登录成功'
    else:
        return '用了get方法，我们应该使用post方法'

'''6+.将返回内容转化为json'''

@app.route('/jsontest')
def jsontest():
    t = {'a':1,'b':'2','c':3}
    return json.dumps(t)



'''7.静态文件'''
#这个文件应该存储在文件系统上的 static/style.css 。
# 也是返回对应文件的地址，这个在templates里的layout.html可见
# url_for('static', filename='style.css')



'''8.模板渲染'''
#Flask配备了Jinja2模板引擎，我们使用render_template()方法来渲染模板
#看后边消息闪现的例子吧，放在了外边是flash_test.py


'''9.访问请求变量'''
#request：全局
#Flask 中的某些对象是全局对象，但却不是通常的那种。这些对象实际上是特定环境的局部对象的代理。
#（1）一个请求传入，Web 服务器决定生成一个新线程, 
#（2）当 Flask 开始它内部的请求处理时,他认为当前线程是一个激活的线程
#（3）并绑定当前的应用和 WSGI 环境到那个线程上，这是一个局部环境

@app.route('/login_n',methods=['GET','POST'])
def login_n():
    if request.method == 'POST':
        #获取post的数据   
        #request.form['username']   request.form.get也可以
        return '使用了post方法'
    else:
        #获取get的数据    http://127.0.0.1:5000/login_n?q=1&d=2
        searchword_q = request.args.get('q', '')
        print(searchword_q)
        searchword_d = request.args.get('d', '')
        print(searchword_d)
        return '使用了get方法'


'''10.文件上传'''
#注意在表单标签中设置enctype="multipart/form-data"
#以上传的文件存放在内存或者文件系统的中的一个临时位置
#我们可以通过请求对象的files属性访问它们，每个上传的文件都会存储在这个字典里



'''
    file_obj = request.files.get("pic")  # "pic"对应前端表单name属性
    if file_obj is None:
        # 表示没有发送文件
        return "未上传文件"
 
    # 将文件保存到本地
    # # 1. 创建一个文件
    # f = open("./demo.png", "wb")
    # # 2. 向文件写内容
    # data = file_obj.read()
    # f.write(data)
    # # 3. 关闭文件
    # f.close()
 
    # 直接使用上传的文件对象保存
    file_obj.save("./demo1.png")
    return "上传成功"
 
'''
@app.route('/upload',methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['txt'] #前端表单name属性
        # 方法一：
        # f.save('/var/www/uploads/uploaded_file.txt')#可以直接save
        # 方法二：
        #你可以直接访问filename属性，但永远不要信任这个值，这个值是可以改的
        #如果你真的要用这个属性，那么请把它传递给 Werkzeug 提供的 secure_filename() 函数:
        #注意先import from werkzeug.utils import secure_filename
        f.save('/var/www/uploads/' + secure_filename(f.filename))
        return '上传成功'



'''11.cookies'''
#注意如果真的需要使用cookies的时候使用密钥签名,不要直接使用
#由于cookies是设置到响应对象上的，而且默认将返回字符串转换为响应对象
#如果想显示的res，注意使用make_response(),和requet同级别引入
@app.route('/cktest')
def cookies_test():
    resp = make_response(render_template('hello.html'))
    resp.set_cookie('username', 'qc')
    username = request.cookies.get('username')
    print(username)

    return resp


'''12.重定向和错误'''
#可以用redirect()函数将用户重定向到其他地方
@app.route('/redi')
def redi():
    #重定向到errtest，url_for的操作对象是方法
    return  redirect(url_for('errtest'))


@app.route('/errtest')
def errtest():
    abort(401)#我们这里主要是为了验证重定向，和简单的重定向到一个不能访问的界面


#默认情况下，错误代码会显示一个黑白的错误，实现情况如下
#如果要定制错误页面，可以使用errorhandler()装饰器
@app.errorhandler(404)
def page_not_find(error):
    return '404'
     #return render_template('page_not_found.html'), 404
     #注意render_template调用之后的404。这告诉flask该页的错误代码是404，即没有找到，默认为200，也就是一切正常

'''13.关于响应
视图函数的返回值会被自动转换为一个响应对象。如果返回值是一个字符串，
它被转换为该字符串为主体的、状态码为 200 OK``的 、 MIME 类型是 ``text/html 的响应对象。Flask 把返回值转换为响应对象的逻辑是这样：

1.如果返回的是一个合法的响应对象，它会从视图直接返回。
2.如果返回的是一个字符串，响应对象会用字符串数据和默认参数创建。
3.如果返回的是一个元组，且元组中的元素可以提供额外的信息。这样的元组必须是 (response, status, headers) 的形式，且至少包含一个元素。
  status 值会覆盖状态代码， headers 可以是一个列表或字典，作为额外的消息标头值。
4.如果上述条件均不满足， Flask 会假设返回值是一个合法的 WSGI 应用程序，并转换为一个请求对象。


so：
如果想在视图里操纵上述步骤结果的响应对象，可以使用make_response()函数
修改上边的例子
@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp

'''

'''14.会话  这个session的实现案例 ，写在外边了，见根目录'''



'''15.消息闪现  这个有时间也写在外边一个demo吧,看外边flash_test.py'''
'''
======================================================================
PS1：分类闪现（要使用一个自定义的分类，只要使用 flash() 函数的第二个参数）
======================================================================
flash(u'Invalid password provided', 'error')

{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    <ul class=flashes>
    {% for category, message in messages %}
      <li class="{{ category }}">{{ message }}</li>
    {% endfor %}
    </ul>
  {% endif %}
{% endwith %}

======================================================================
PS2:过滤闪现消息
======================================================================

{% with errors = get_flashed_messages(category_filter=["error"]) %}
{% if errors %}
<div class="alert-message block-message error">
  <a class="close" href="#">×</a>
  <ul>
    {%- for msg in errors %}
    <li>{{ msg }}</li>
    {% endfor -%}
  </ul>
</div>
{% endif %}
{% endwith %}



'''





'''16.日志记录'''
current_app.logger.debug('A Value For debugging')
current_app.logger.warning('A warning occurred (%d apples)', 42)
current_app.logger.error('An error occurred')


'''17.整合 WSGI中间件'''
# 如果你想给你的应用添加 WSGI 中间件，你可以封装内部 WSGI 应用。
# 例如若是你想用 Werkzeug 包中的某个中间件来应付 lighttpd 中的 bugs ，
# 可以这样做:

# from werkzeug.contrib.fixers import LighttpdCGIRootFix
# app.wsgi_app = LighttpdCGIRootFix(app.wsgi_app)








if __name__ == '__main__':
    #使服务器公开可用的方法 app.run(host = '0.0.0.0', port = '8080')
    app.run(debug=True)#调试模式，注意设置生产不可用

