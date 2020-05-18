from flask import Flask,url_for,redirect
 
app = Flask ("my-app")
 
 
@app.route ('/<name>')
def hello_world(name):
    return 'Hello World,My name is %s!' %name
 
@app.route('/test/<name>')
def test(name):
    #用于构建指定函数的url，操作对象是函数，而不是route里的路径
    #返回值是对应方法名，所指向的路由地址
    # 一般和重定向搭配使用，得到对应方法的路径地址，重定向回去
    return redirect(url_for('hello_world',name=name))
 
if __name__ == '__main__':
    app.run (debug=True)
