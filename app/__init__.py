#encoding=utf-8
#! env/bin/python

from flask import Flask

app = Flask(__name__)

# app/views.py
from app import views
