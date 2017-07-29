from argparse import ArgumentParser
from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import settings
import time
import profiler

app = Flask(__name__)

def picked_up():
    messages = [
        "こんにちは，あなたの名前を入力してください",
        "やあ！お名前はなんですか？",
        "あなたの名前を教えてね"
    ]
    return np.random.choice(messages)

@app.route('/', methods=['GET'])
def index():
    message = picked_up()
    return render_template("index.html",message=message,title=settings.TITLE)

@app.route('/post',methods=['GET','POST'])
def post():
    if request.method =="POST":
        name = request.form['name']
        profiler.from_user_id()
        return render_template('index.html',name=name,title=settings.TITLE)
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()


    app.run(debug=options.debug, port=options.port)
