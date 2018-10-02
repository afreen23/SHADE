import twitter
import json
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import NaturalLanguageUnderstandingV1 
from watson_developer_cloud.natural_language_understanding_v1 import Features, SentimentOptions, EmotionOptions
from watson_developer_cloud import WatsonApiException
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome"

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-03-16',
    username='c5fa57b9-d66e-4443-95b0-5bce1319419f',
    password='bbeFpb3BGQ4c',
    url='https://gateway.watsonplatform.net/natural-language-understanding/api'
)

tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    username='fe7d6f8f-52d1-49a3-a129-cef7fbeeb936',
    password='ps3wXtMa2br6',
    url='https://gateway.watsonplatform.net/tone-analyzer/api'
)

api = twitter.Api(consumer_key='YecKuKjZfTp6nd2HbEQlTitPh',
  consumer_secret='vs7YRFW9bgZPrQaRF02A42eb918jBpWrsXolVY8OX9FztL6Iyf',
  access_token_key='876676220053848065-8kIAIn9glBEXfvUx0LwRI8UzGi9HMo6',
  access_token_secret='D987liyrt7b5XDDXZnraGQMbRvOipoBmSyhr5eXt6zpnR')

t=api.GetUserTimeline(screen_name="BBCWorld",count =20,include_rts=False,exclude_replies=True)

print("---------Tweet coming in----------")



def tone_analysis(tweet):
    analysed_tones =[]  
    try:
        # Invoke a Tone Analyzer method
        tone_analysis = tone_analyzer.tone(
        {'text': tweet.text},
        'application/json'
    ).get_result()
    except WatsonApiException as ex:
        print("Method failed with status code " + str(ex.code) + ": " + ex.message)
    tones = tone_analysis['document_tone']['tones']
    for tone in tones:
        if tone["score"]>=0.75:
            analysed_tones.append({'tone':tone["tone_name"],'score':tone['score']})
    return analysed_tones

def nlu_analysis(tweet):
    response=''
    try:
        response = natural_language_understanding.analyze(
        text=tweet,
        features=Features(
            emotion=EmotionOptions(),
            sentiment=SentimentOptions()
            )).get_result()
    except WatsonApiException as ex:
        print("Method failed with status code " + str(ex.code) + ": " + ex.message)
    return response

for tweet in t:
    print("\n----------Tweet:------------\n")
    print(tweet.text)
    analysis=tone_analysis(tweet)
    print("------------Tone Analysis----------\n")
    print(json.dumps({'tones': analysis}, indent=2))
    print("\n-----------NLP Analysis-------------------\n")
    response = nlu_analysis(tweet.text)
    print(json.dumps(response, indent=2))
    print("--------------")
