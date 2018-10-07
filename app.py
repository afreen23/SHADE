from flask import Flask,redirect,url_for,jsonify,render_template
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_cors import CORS,cross_origin
# from flask_restful import Resource,Api
#from flask_dance.contrib.facebook import make_facebook_blueprint, facebook

app = Flask(__name__)
CORS(app)
twitter_blueprint = make_twitter_blueprint(api_key='YecKuKjZfTp6nd2HbEQlTitPh',api_secret='vs7YRFW9bgZPrQaRF02A42eb918jBpWrsXolVY8OX9FztL6Iyf')
app.register_blueprint(twitter_blueprint,url_prefix='/login')

#facebook_blueprint = make_facebook_blueprint(client_id=None, client_secret=None, scope=None, redirect_url=None, redirect_to=None, login_url=None, authorized_url=None, session_class=None, backend=None)

@app.route('/')
def home():
    return "Success"

@app.route('/twitter')
def get():
    if not twitter.authorized:
        return redirect(url_for("twitter.login"))
    resp = twitter.get("account/settings.json")
    resp = twitter.get("statuses/user_timeline.json")
    assert resp.ok
    return {'message':"You are @{screen_name} on Twitter".format(screen_name=resp.json()["screen_name"])},200


if __name__ == '__main__':
    app.run(debug=True)