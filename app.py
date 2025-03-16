import tweepy
import argparse
import webbrowser
import json
from pythonosc import udp_client
# from flask import Flask, request
app = Flask(__name__)
at = "udUcuD2dicPTciDrjr5HgGHIO"
ats = "X5V8AukObOXdcGl1GHnjowNHVLlbknBwJNdA0XDVPnjECcuu6d"
try:
    f = open(".token_config", "r")
    # i = open(".two_token_config", "r")
    user_at, user_ats = json.load(f)
    # access_token = json.load(i)
except:
    oauth1_user_handler = tweepy.OAuth1UserHandler(
        at, ats,
        callback="oob"
    )
    webbrowser.open(oauth1_user_handler.get_authorization_url(signin_with_twitter=True))
    user_at, user_ats = oauth1_user_handler.get_access_token(
        input("Input PIN: ")
    )
    print([user_at, user_ats])
    f = open(".token_config", "w")
    json.dump([user_at, user_ats], f)
    # oauth2_user_handler = tweepy.OAuth2UserHandler(
    #     client_id="NVRVZ3JteVQ0UU9CUTRTeEpFNkc6MTpjaQ",
    #     redirect_uri="http://localhost:5000/auth",
    #     scope=["tweet.write", "offline.access", "media.write"],
    #     client_secret="FeaCseXV_2YdRBpLEJRau088c85jjlrk8t6f-G90wGeCoB8e4l"
    # )
    # webbrowser.open(oauth2_user_handler.get_authorization_url(), new=0, autoraise=True)
auth = tweepy.OAuth1UserHandler(at, ats, user_at, user_ats)
api = tweepy.API(auth)

@app.route('/')
def hello():
    return "Hello World"

@app.route('/upload')
def upload():
    global at
    global ats
    global user_at
    global user_ats
    # global access_token
    # if not ('access_token' in globals()):
    #     response = oauth2_user_handler.fetch_token(
    #         request.url.replace('http', 'https')
    #     )
    #     access_token = response["access_token"]
    #     f = open(".two_token_config", "w")
    #     json.dump([access_token], f)
    img = api.media_upload("D:\\Pictures\\Screenshots\\スクリーンショット 2024-09-18 224413.png")
    client = tweepy.Client(consumer_key=at, consumer_secret=ats, access_token=user_at, access_token_secret=user_ats)
    client.create_tweet(text="Hello!", media_ids=[img.media_id])
    return "Sucess"

@app.route('/Screen')
def Screen():
    client = udp_client.SimpleUDPClient('127.0.0.1', 9000)

    key_input = input("1か0の数字を入れてください: ")
    key_input = float(key_input)
    client.send_message("/avatar/parameters/ScreenY", key_input)
    return "Success"

if __name__ == "__main__":
    app.run(debug=True, port=8888, threaded=True)

