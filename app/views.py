#encoding=utf-8

# 模板默认的目录为app/templates
from flask import render_template, flash, redirect
from app import app

# 从forms.py中引入LoginForm
from forms import LoginForm

# 让/和/index都调用index函数
@app.route('/')
@app.route('/index')
def index():
    user  = {'nickname':'Oleyang'}
    posts = [
        {
            'author': {'nickname':'John'},
            'body': "beautiful day in Portland!",
        },
        {
            'author': {'nickname':'Susan'},
            'body': "The Avengers movie was so cool!",
        },
    ]
    return render_template('index.html',
                           title='Microblog Home',
                           user=user,
                           posts=posts
                           )

# 只允许get和post请求
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # 点击的提交按钮
    if form.validate_on_submit():
        flash('login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data))
          )
        return redirect('login')
    return render_template('login.html',
                           form = form,
                           title = 'Sign In',
                           providers=app.config['OPENID_PROVIDERS']
                           )
