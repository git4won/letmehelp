# coding=utf-8

from flask import url_for
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    # name = "vin"
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
