from flask import Flask,redirect,url_for,render_template
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from keys import CONSUMER_KEY, CONSUMER_SECRET_KEY
#from flask_dance.contrib.facebook import make_facebook_blueprint, facebook

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thissupposedtobesecret'

twitter_blueprint = make_twitter_blueprint(api_key=CONSUMER_KEY,api_secret=CONSUMER_SECRET_KEY)
app.register_blueprint(twitter_blueprint,url_prefix='/login')

#facebook_blueprint = make_facebook_blueprint(client_id=None, client_secret=None, scope=None, redirect_url=None, redirect_to=None, login_url=None, authorized_url=None, session_class=None, backend=None)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/twitter")
def twitter_login():
    if not twitter.authorized:
        return redirect(url_for("twitter.login"))
    resp = twitter.get("account/settings.json")
    assert resp.ok
    return "You are @{screen_name} on Twitter".format(screen_name=resp.json()["screen_name"])

if __name__ == '__main__':
    app.run()