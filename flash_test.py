from flask import Flask,flash,redirect,render_template,\
    request,url_for

app = Flask(__name__)
app.secret_key = 'some_secret'
#test1
#test2
#首页
@app.route('/')
def index():
    return render_template('index.html')


#登录
@app.route('/login',methods=['GET','POSt'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
            request.form['password'] != '123456':
            error = "Invalid credentials"
        else:
            flash('You were successfully logged in')
            return redirect(url_for('index'))
    #如果没有正常返回，把error放回去
    return render_template('login.html', error=error)


if __name__ == "__main__":
    app.run(debug=True)