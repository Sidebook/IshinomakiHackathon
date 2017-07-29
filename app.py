from argparse import ArgumentParser
from flask import Flask, render_template, request, redirect, url_for

from exceptions import UserNotFoundException, UnauthorizedException, InsufficientTweetsError
import numpy as np
import settings
import time
import profiler

app = Flask(__name__)

HOME_HTML = 'index.html'

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
    """ポストに対する応答

    keywords to jinja2
        user_id_man: 男性のユーザーID
        user_id_woman: 女性のユーザーID
        error: エラーが起きたかどうか
        error_message: エラーの説明文
        profiled: プロファイルが成功したかどうか
        personality: 解析結果のうち、「個性」を表すリスト。個々の要素は name(項目名) man(男性側の値) woman(女性側の値) のキーを持つ辞書
        values_man: 解析結果のうち、男性側の「価値」を表すリスト、大きい順にソートされており、各要素は長さ２のタプル。第１要素が項目名、第２要素が値
        values_man: 解析結果のうち、女性側の「価値」を表すリスト、大きい順にソートされており、各要素は長さ２のタプル。第１要素が項目名、第２要素が値
    """
    if request.method =="POST":
        man = request.form['id_man']
        #print(man)
        woman = request.form['id_woman']
        #print(woman)

        compatibility = ''
        profiled = False
        error = True
        error_message = ''
        processing_id = man

        if man == '':
            error_message = '診断したい男性の Twitter ID を入力してください'
        elif woman == '':
            error_message = '診断したい女性の Twitter ID を入力してください'
        if man == '' or woman == '':
            return render_template(HOME_HTML,
                profiled=False,
                error=error,
                error_message=error_message,
                user_id_man=man,
                user_id_woman=woman)

        try:
            profile_man = profiler.from_user_id(man)
            processing_id = woman
            profile_woman = profiler.from_user_id(woman)
            compatibility = '{0:.1f} %'.format(profile_man.compare(profile_woman) * 100)
            profiled = True
            error = None
        except UserNotFoundException as e:
            compatibility = '??'
            error_message = 'ユーザー @{} は存在しません。'.format(processing_id)
        except UnauthorizedException as e:
            compatibility = '??'
            error_message = 'ユーザー @{} は非公開です。'.format(processing_id)
        except InsufficientTweetsError as e:
            compatibility = '??'
            error_message = 'ユーザー @{} のツイートから十分なデータを取得できません。'.format(processing_id)
        if profiled:
            personality = []
            for k, v in profile_man.personality.items():
                man_p = '{0:.1f} %'.format(v * 100)
                woman_p = '{0:.1f} %'.format(profile_woman.personality[k] * 100)
                personality.append({'name': k, 'man': man_p, 'woman': woman_p})
            
            values_man = sorted(profile_man.values.items(), key=lambda x:x[1], reverse=True)
            values_woman = sorted(profile_woman.values.items(), key=lambda x:x[1], reverse=True)
            values_man = [(v[0], '{0:.1f} %'.format(v[1] * 100)) for v in values_man]
            values_woman = [(v[0], '{0:.1f} %'.format(v[1] * 100)) for v in values_woman]
            print(values_man)
            print(values_woman)

            return render_template(
                HOME_HTML,
                profiled=True,
                personality=personality,
                values_man=values_man,
                values_woman=values_woman,
                compatibility=compatibility,
                user_id_man=man,
                user_id_woman=woman
            )
        else:
            return render_template(HOME_HTML,
            profiled=False,
            error=error,
            error_message = error_message,
            user_id_man=man,
            user_id_woman=woman)
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
