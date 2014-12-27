# -*- coding: utf-8 -*-

import os


from flask import Flask

CHRYSOLOPHUS_PROJECT_ROOT_DIR = os.environ['CHRYSOLOPHUS_PROJECT_ROOT_DIR']
STATIC_HTML_DIR = os.path.join(CHRYSOLOPHUS_PROJECT_ROOT_DIR, 'static/html')

app = Flask(__name__, static_url_path=STATIC_HTML_DIR)

@app.route('/')
def weekly_summary():
    today_html = os.path.join(STATIC_HTML_DIR, 'today.html')
    return app.send_static_file(today_html)

if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=8000
    )
