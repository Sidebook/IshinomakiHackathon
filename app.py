from argparse import ArgumentParser
from flask import Flask, render_template, request, redirect, url_for

from exceptions import UserNotFoundException, UnauthorizedException, InsufficientTweetsError
import numpy as np
import settings
import time
import profiler

app = Flask(__name__)

HOME_HTML = 'ishinomakihackathon.html'

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
    return render_template(HOME_HTML, message=message,title=settings.TITLE)

@app.route('/post',methods=['GET','POST'])
def post():
    if request.method =="POST":
        man = request.form['id_man']
        #print(man)
        woman = request.form['id_woman']
        #print(woman)

        compatibility = ''
        profiled = False
        try:
            profile_man = profiler.from_user_id(man)
            profile_woman = profiler.from_user_id(woman)
            compatibility = str(profile_man.compare(profile_woman) * 100) + ' %'
            profiled = True
        except UserNotFoundException as e:
            compatibility = 'ユーザーが見つかりません'
        except UnauthorizedException as e:
            compatibility = '非公開アカウントです'
        except InsufficientTweetsError as e:
            compatibility = 'ツイートが少なすぎます'
        if profiled:
            profile = []
            for k, v in profile_man.personality.items():
                man_p = '{0:.1f} %'.format(v * 100)
                woman_p = '{0:.1f} %'.format(profile_woman.personality[k] * 100)
                profile.append({'name': k, 'man': man_p, 'woman': woman_p})
            
            return render_template(
                HOME_HTML,
                profiled=True,
                profile=profile
            )
        else:
            return render_template(HOME_HTML)
    else:
        return redirect(url_for(HOME_HTML))

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()


    app.run(debug=options.debug, port=options.port)
