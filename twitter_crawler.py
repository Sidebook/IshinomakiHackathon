# -*- coding: utf-8 -*-
from exceptions import UserNotFoundException

def crawl(user_id, minlength=1500):
    """user_id で指定されたアカウントのツイートをクロールします。
    user_id は先頭に '@' を含まない形式で指定してください。

    :params user_id: ユーザーID
    :return: ユーザーIDのクローリング結果
    """

    # もしuser_idのアカウントが存在しない場合、UserNotFoundExceptionを投げる
    # こんな感じ↓
    # raise UserNotFoundException()

    return 'description of {}'.format(user_id)

# こっから下は、このプログラム自体がスクリプトとして実行された場合の処理
# ユーザーIDを聞いて、data/{user_id}.txt に結果を保存する。
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
            with open('data/{}.txt'.format(user_id), 'w') as f:
                f.write(result)
        except UserNotFoundException as e:
            print('\033[031muser \'@{}\' doesn\'t exists. Or this is a private account.\033[0m'.format(user_id))
            success = False
        except Exception as e:
            print('\033[031msomething goes wrong: {}\033[0m'.format(e))
            success = False

        if success:
            print('saved: {}'.format(path))
        
if __name__ == '__main__':
    main()
