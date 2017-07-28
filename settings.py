import os

PERSONALITY_INSIGHTS_USERNAME = os.getenv('PERSONALITY_INSIGHTS_USERNAME', default='')
if PERSONALITY_INSIGHTS_USERNAME == '':
    print('please set enviroment value PERSONALITY_INSIGHTS_USERNAME')

PERSONALITY_INSIGHTS_PASSWORD = os.getenv('PERSONALITY_INSIGHTS_PASSWORD', default='')
if PERSONALITY_INSIGHTS_PASSWORD == '':
    print('please set enviroment value PERSONALITY_INSIGHTS_PASSWORD')

TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY', default='')
if TWITTER_CONSUMER_KEY == '':
    print('please set enviroment value TWITTER_CONSUMER_KEY')

TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET', default='')
if TWITTER_CONSUMER_SECRET == '':
    print('please set enviroment value TWITTER_CONSUMER_KEY')

TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN', default='')
if TWITTER_ACCESS_TOKEN == '':
    print('please set enviroment value TWITTER_ACCESS_TOKEN')

TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET', default='')
if TWITTER_ACCESS_TOKEN_SECRET == '':
    print('please set enviroment value TWITTER_ACCESS_TOKEN_SECRET')
