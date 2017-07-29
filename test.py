from flask import Flask, render_template
from argparse import ArgumentParser

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',
            profiled=True,
            personality=[{'name':'知的好奇心', 'man':'82.2 %', 'woman':'43.2%'}],
            values_man=[('快楽主義','43.2%')],
            values_woman=[('快楽主義','43.2%')],
            compatibility='99.9%',
            user_id_man='id_of_man',
            user_id_woman='id_of_woman',
            comment='ここにこめんとが入ります',
            compatible_level=0
        )

if __name__ == '__main__':
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)