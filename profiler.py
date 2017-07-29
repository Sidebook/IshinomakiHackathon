import settings
import requests
import json
import os
import math
import twitter_crawler as tw
import re

from exceptions import UserNotFoundException, UnauthorizedException, InsufficientTweetsError

from watson_developer_cloud import PersonalityInsightsV3

personality_insights = PersonalityInsightsV3(
    version='2016-10-20',
    username=settings.PERSONALITY_INSIGHTS_USERNAME,
    password=settings.PERSONALITY_INSIGHTS_PASSWORD
)

class Profile():
    def __init__(
        self,
        user_id=None,
        personality=None):
        
        self.user_id = user_id
        self.personality = personality
    
    def __str__(self):
        s = 'user id: {}'.format(
            self.user_id,
        )
        for k, v in self.personality.items():
            s += '\n{}: {}'.format(k, v)

        return s

    def compare(self, another):
        """
        dot = 0
        self_length = 0
        another_length = 0
        for k, self_v in self.personality.items():
            if k not in another.personality:
                raise Exception()
                return 0
            another_v = another.personality[k]
            dot += self_v * another_v
            self_length += self_v * self_v
            another_length += another_v * another_v
        
        self_length = math.sqrt(self_length)
        another_length = math.sqrt(another_length)

        cos = dot / (self_length * another_length)

        return cos
        """

        n = len(self.personality)
        delta = 0
        for k, self_v in self.personality.items():
            if k not in another.personality:
                raise Exception()
                return 0
            another_v = another.personality[k]
            delta += abs(self_v - another_v)
        delta /= n

        return 1 - delta
    
def from_text(text):
    profile_json = personality_insights.profile(
        text=text,
        content_type='text/plain',
        raw_scores=False,
        consumption_preferences=False,
        csv_headers=False,
        content_language='ja',
        accept_language='ja'
    )
    
    personality = profile_json['personality']

    openness = 0
    conscientiousness = 0
    extraversion = 0
    agreeableness = 0
    neuroticism = 0

    for p in personality:
        trait_id = p['trait_id']
        if (trait_id == 'big5_openness'):
            openness = p['percentile']
        elif (trait_id == 'big5_conscientiousness'):
            conscientiousness = p['percentile']
        elif (trait_id == 'big5_extraversion'):
            extraversion = p['percentile']
        elif (trait_id == 'big5_agreeableness'):
            agreeableness = p['percentile']
        elif (trait_id == 'big5_neuroticism'):
            neuroticism = p['percentile']

    profile = Profile(
        personality={
            '知的好奇心':openness,
            '誠実性':conscientiousness,
            '外向性':extraversion,
            '協調性':agreeableness,
            '感情起伏':neuroticism
        }
    )

    return profile


def from_user_id(user_id):
    tweets = tw.crawl(user_id)
    tweets = re.sub('@[^\s]*\s', '', tweets)
    tweets = re.sub('https://[^\s]*\s', '', tweets)
    tweets = re.sub('http://[^\s]*\s', '', tweets)
    if len(tweets) < 1500:
        raise InsufficientTweetsError()
    
    profile = from_text(tweets)
    profile.user_id = user_id
    return profile


def main():
    while True:
        try:
            print('please input the man\'s twitter user ID.')
            user_id = input('>>> ')
            if not user_id:
                return
            profile_man = from_user_id(user_id)
            print(profile_man)

            print('please input the woman\'s twitter user ID.')
            user_id = input('>>> ')
            if not user_id:
                return
            profile_woman = from_user_id(user_id)
            print(profile_woman)

            print(profile_man.compare(profile_woman))
        except UserNotFoundException as e:
            print('\033[31;40mUser @{} not found.\033[0m'.format(user_id))
        except UnauthorizedException as e:
            print('\033[31;40mUser @{} is private.\033[0m'.format(user_id))
        except InsufficientTweetsError as e:
            print('\033[31;40mthe number of words tweeted by User @{} is insufficient.\033[0m'.format(user_id))

if __name__ == '__main__':
    main()
