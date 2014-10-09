#encoding=utf-8

# 模板默认的目录为app/templates
from flask import render_template

from app import app

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
