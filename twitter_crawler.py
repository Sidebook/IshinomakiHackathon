# -*- coding: utf-8 -*-
from exceptions import UserNotFoundException, UnauthorizedException
import json
import settings
from requests_oauthlib import OAuth1Session
import time

#　TwitterのAPIで必須になる４つのアクセスキーをここで定義．詳細な情報をgithubにあげるとやばいから，settingsファイルに入れて環境変数にしている．
url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
CK = settings.TWITTER_CONSUMER_KEY
CS = settings.TWITTER_CONSUMER_SECRET
AT = settings.TWITTER_ACCESS_TOKEN
ATS = settings.TWITTER_ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)

def crawl(user_id, minlength=20000):
    """user_id で指定されたアカウントのツイートをクロールします。
    user_id は先頭に '@' を含まない形式で指定してください。

    :params user_id: ユーザーID screen_name: そのユーザーIDの人のツイートを取得 count: 一回のスクレイピングでとって来るツイートの数 include_rts: リツイートを消す
    :result: クローリングして得られたテキストデータを足していく
    :return: ユーザーIDのクローリング結果
    """
    result = ''
    params = {'screen_name' : user_id, 'count' : 200, 'include_rts' : False} 
    req = twitter.get(url, params = params)

    if req.status_code == 200:
        for i in range(16):
            tweets = json.loads(req.text)
            # print('get {} tweets of @{}'.format(len(tweets), user_id))
            for tweet in tweets:
                result += tweet['text'] + "\n"
            if len(tweets) == 0:
                return result
            ID = tweets[-1]['id']
            # print(ID)
            params['max_id'] = ID - 1
            req = twitter.get(url, params = params)
            if len(result) > minlength :
                # print(len(result))
                return result
            time.sleep(1)
        return result
    elif req.status_code == 401:
        raise UnauthorizedException()
    elif req.status_code == 404:
        raise UserNotFoundException(message='user @{} not found.'.format(user_id))


# こっから下は、このプログラム自体がスクリプトとして実行された場合の処理
# 何も入力しないでエンターで終了

def main():
    while True:
        print('please input user name. (except \'@\') Pless Enter to exit.')
        user_id = input('>>> ')
        if not user_id:
            return

        success = True
        path = 'data/{}.txt'.format(user_id)
        try:
            result = crawl(user_id)
            print(result)
        except UserNotFoundException as e:
            print('\033[031m404 user \'@{}\' doesn\'t exists.\033[0m'.format(user_id))
            success = False
        except UnauthorizedException as e:
            print('\033[031m401 this channel is private.\033[0m')
            success = False
        #except Exception as e:
        #    print('\033[031msomething goes wrong: {}\033[0m'.format(e))
        #    success = False
        
if __name__ == '__main__':
    main()
