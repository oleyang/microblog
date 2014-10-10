#encoding=utf-8

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-wil-never-guess'


OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}
]
