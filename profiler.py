import settings
import requests
import json
import os

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
        openness=0,
        conscientiousness=0,
        extraversion=0,
        agreeableness=0,
        neuroticism=0):
        
        self.user_id = user_id
        self.openness = openness
        self.conscientiousness = conscientiousness
        self.extraversion = extraversion
        self.agreeableness = agreeableness
        self.neuroticism = neuroticism
    
    def __str__(self):
        s = 'user id: {}\n' \
        '知的好奇心: {}\n' \
        '誠実性: {}\n' \
        '外向性: {}\n' \
        '協調性: {}\n' \
        '感情起伏: {}'.format(
            self.user_id,
            self.openness,
            self.conscientiousness,
            self.extraversion,
            self.agreeableness,
            self.neuroticism
        )

        return s

    def compare(self, another):
        return 0.6

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
        openness=openness,
        conscientiousness=conscientiousness,
        extraversion=extraversion,
        agreeableness=agreeableness,
        neuroticism=neuroticism
    )

    return profile

def main():
    while True:
        print('please input text file.')
        path = input('>>> ')
        if not path:
            return
        
        try:
            with open(path, 'r') as f:
                text = str(f.read())
                profile = from_text(text)
            
            with open(path + 'profile.txt', 'w') as f:
                print(profile)

        except Exception as e:
            print('\033[31;40msomething goes wrong: {}\033[0m'.format(e))

if __name__ == '__main__':
    main()
