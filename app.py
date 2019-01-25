from flask import Flask, json, request, render_template
import tweepy

app = Flask(__name__)

app.config.from_object('config')
auth = tweepy.OAuthHandler(app.config['TWITTER_CONSUMER_KEY'],
                           app.config['TWITTER_CONSUMER_SECRET'])
auth.set_access_token(app.config['TWITTER_ACCESS_TOKEN'],
                      app.config['TWITTER_ACCESS_TOKEN_SECRET'])
tweepy_api = tweepy.API(auth)

def get_tweets(username):
    tweets = tweepy_api.user_timeline(screen_name=username)                                                                            
    return [{'content': tweet.text,
              'created_at': tweet.created_at,
              'username': username,
              'headshot_url': tweet.user.profile_image_url}
           for tweet in tweets]

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def tweets():
    username = request.form['username']
    try:
        return render_template("tweets.html", tweets=get_tweets(username))
    except Exception as e:
        return render_template("404.html")

app.run(debug=True, port=8080)