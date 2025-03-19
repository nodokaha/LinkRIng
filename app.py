import tweepy
import argparse
import webbrowser
import json
from pythonosc import udp_client
at = "udUcuD2dicPTciDrjr5HgGHIO"
ats = "X5V8AukObOXdcGl1GHnjowNHVLlbknBwJNdA0XDVPnjECcuu6d"
try:
    f = open(".token_config", "r")
    user_at, user_ats = json.load(f)
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
auth = tweepy.OAuth1UserHandler(at, ats, user_at, user_ats)
api = tweepy.API(auth)

def SettingImageList(media_path_list):
    media_list = []
    for x in media_path_list:
        img = api.media_upload("D:\\Pictures\\Screenshots\\スクリーンショット 2024-09-18 224413.png")
        media_list += img.media_id
    return media_list

def Touch(message, media_list):
    client = tweepy.Client(consumer_key=at, consumer_secret=ats, access_token=user_at, access_token_secret=user_ats)
    client.create_tweet(text=message, media_ids=media_list)

def Screen():
    client = udp_client.SimpleUDPClient('127.0.0.1', 9000)

    key_input = input("1か0の数字を入れてください: ")
    key_input = float(key_input)
    client.send_message("/avatar/parameters/ScreenY", key_input)

