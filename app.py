import twitter
import json
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import NaturalLanguageUnderstandingV1 
from watson_developer_cloud.natural_language_understanding_v1 import Features, SentimentOptions, EmotionOptions
from watson_developer_cloud import WatsonApiException
from flask import Flask,request
from keys import NLP_USERNAME,NLP_PASSWORD,TONE_USERNAME,TONE_PASSWORD,CONSUMER_KEY,CONSUMER_SECRET_KEY,ACCESS_TOKEN_KEY,ACCESS_TOKEN_SECRET
from flask import render_template

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-03-16',
    username=NLP_USERNAME,
    password=NLP_PASSWORD,
    url='https://gateway.watsonplatform.net/natural-language-understanding/api'
)

tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    username=TONE_USERNAME,
    password=TONE_PASSWORD,
    url='https://gateway.watsonplatform.net/tone-analyzer/api'
)

api = twitter.Api(consumer_key=CONSUMER_KEY,
  consumer_secret=CONSUMER_SECRET_KEY,
  access_token_key=ACCESS_TOKEN_KEY,
  access_token_secret=ACCESS_TOKEN_SECRET)


app = Flask(__name__)

TWITTER_HANDLE=''

@app.route('/')
#home page
def index():
    return render_template('index.html')

@app.route('/home',methods=['GET','POST'])
#sentiment analysis
def sentiment_analysis():
    request_data=request.get_json()
    TWITTER_HANDLE=request_data['name']
    t=api.GetUserTimeline(screen_name=TWITTER_HANDLE,count =2,include_rts=False,exclude_replies=True)
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
    return "Success"


    #tone analysis
    def tone_analysis(tweet):
        analysed_tones =[]  
        try:
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

    #nlu analysis
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

app.run()