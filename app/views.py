#encoding=utf-8

# 模板默认的目录为app/templates
from flask import render_template, flash, redirect,session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
# 从forms.py中引入LoginForm
from forms import LoginForm

from models import User

import inspect

def get_current_function_name():
    return inspect.stack()[1][3]

# 让/和/index都调用index函数
@app.route('/')
@app.route('/index')
@login_required
def index():
    # g是flask中的全局变量，在一个request生命周期中，用来存储和共享数据的变量
    user = g.user
    #user  = {'nickname':'Oleyang'}
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
                           posts=posts,
                           nav = {
                               'link':'/index',
                               'title' : 'index',   
                               }
                           )

# 登录之前都要执行这个函数
@app.before_request
def befor_request():
    # 把当前用户的信息存在在全局的变量g中
    g.user = current_user

# 只允许get和post请求
@app.route('/login', methods=['GET', 'POST'])
# 告诉Flask-OpenID，下面的函数是login的view
@oid.loginhandler
def login():
    # 如果已经登录就跳转到index
    # g在哪里？
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
        
    form = LoginForm()
    # 点击的提交按钮
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])

        # 
        # flash('login requested for OpenID="%s", remember_me=%s' %
        #       (form.openid.data, str(form.remember_me.data))
        #   )
        # return redirect('login')
    return render_template('login.html',
                           form = form,
                           title = 'Sign In',
                           providers=app.config['OPENID_PROVIDERS'],
                           nav = {
                               'link':'/login',
                               'title' : get_current_function_name(),   
                               }
                           )

# 登录成功以后，主要是对session的处理
@oid.after_login
def after_login(resp):
    # 没有输入email
    if resp.email is None or resp.email == '':
        # 输出提示内容
        flash("Invalid Login (email is none), Please relogin")
        return redirect(url_for('login'))

    user = User.query.filter_by(email==resp.email).first()

    # 新用户
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == '':
            nickname = resp.email.split('@')[0]

        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()

    # session 处理
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)

    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

#  login out
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    
# 从数据库中查找用户的信息 
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
