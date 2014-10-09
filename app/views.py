#encoding=utf-8

from app import app

# 让/和/index都调用index函数
@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!(世界，我来了！)"
