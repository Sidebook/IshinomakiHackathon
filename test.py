from flask import Flask, render_template
from argparse import ArgumentParser

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html',
            profiled=True,
            personality=[
                {'name':'知的好奇心', 'man':'82%', 'woman':'63%'},
                {'name':'誠実性', 'man':'97%', 'woman':'43%'},
                {'name':'外向性', 'man':'10%', 'woman':'19%'},
                {'name':'協調性', 'man':'21%', 'woman':'26%'},
                {'name':'感情起伏', 'man':'13%', 'woman':'62%'}
                ],
            values_man=[('快楽主義','99%'), ('自己超越','40%'), ('現状維持','32%'), ('変化許容性','11%'), ('自己増進','5%')],
            values_woman=[('快楽主義','80%'), ('自己超越','62%'), ('現状維持','43%'), ('変化許容性','21%'), ('自己増進','10%')],
            compatibility='99.9%',
            user_id_man='id_of_man',
            user_id_woman='id_of_woman',
            comment='ここにこめんとが入ります',
            compatible_level=2,
            tooltip={
                '知的好奇心':'落ち着きがあり，美に敏感で新しいことを試そうとするタイプ',
                '誠実性':'自己統制をし、誠実、あるいは外部の期待や評価に応えようとするタイプ',
                '外向性':'よりエネルギッシュで，社交的なタイプ',
                '協調性':'他人とうまくやっていくことを重要視するタイプ',
                '感情起伏':'感情の幅に大きな動きがあるタイプ',
                '自己増進':'社会的な基準に基づく個人的な成功',
                '自己超越':'身の回りの人をより幸せにしようとする',
                '現状維持':'伝統を重んじる保守的な姿勢',
                '変化許容性':'日常生活において興奮や新規性を追い求める',
                '快楽主義':'自分自身の幸福や満足感'
            }
        )

if __name__ == '__main__':
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)