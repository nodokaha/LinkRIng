# -*- coding: utf-8 -*-
import tweepy
import argparse
import webbrowser
import json
from datetime import datetime
import ctypes.wintypes
import os
from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
from pathlib import Path

at = "udUcuD2dicPTciDrjr5HgGHIO"
ats = "X5V8AukObOXdcGl1GHnjowNHVLlbknBwJNdA0XDVPnjECcuu6d"
client = udp_client.SimpleUDPClient('127.0.0.1', 9000)
message = "test Message"
try:
    f = open(".token_config", "r")
    user_at, user_ats = json.load(f)
    print("Load Success...!!")
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

def SettingImageList():
    CSIDL_MYPICTURES = 0x27
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_MYPICTURES, 0, 0, buf)
    picture_folder = list(Path(buf.value + '/VRChat/' + datetime.now().strftime("%Y-%m")).glob(r'*.png'))
    picture_folder.sort(key=os.path.getctime, reverse=True)
    media_path_list = [picture_folder[0]]
    media_list = []
    Screen(0.25, 1)
    for x in media_path_list:
        img = api.media_upload(x.resolve())
        media_list += [img.media_id]
        print(x.resolve())
    return media_list

def TweetPost(message, media_list):
    client = tweepy.Client(consumer_key=at, consumer_secret=ats, access_token=user_at, access_token_secret=user_ats)
    client.create_tweet(text=message, media_ids=media_list)
    Screen(0.5, 1)

def Screen(x, y):
    client.send_message("/avatar/parameters/ScreenX", x)
    client.send_message("/avatar/parameters/ScreenY", y)

def Touch(unused_addr, args, touch_flag):
    if touch_flag:
        client.send_message("/avatar/parameters/Check", True)
        Screen(0.25, 1.0)

def Check(unused_addr, args, touch_flag):
    if touch_flag:
        client.send_message("/avatar/parameters/Check", False)
        TweetPost(message, SettingImageList())
        Screen(0.5, 1.0)

def TouchOne(unused_addr, args, touch_flag):
    global message
    if touch_flag:
        message = "One Test Message"

def TouchTwo(unused_addr, args, touch_flag):
    global message
    if touch_flag:
        message = "Two Test Message"

def TouchThree(unused_addr, args, touch_flag):
    global message
    if touch_flag:
        message = "Three Test Message"

def TouchFour(unused_addr, args, touch_flag):
    global message
    if touch_flag:
        message = "Four Test Message"

def TouchFive(unused_addr, args, touch_flag):
    global message
    if touch_flag:
        message = "Five Test Message"

def TouchSix(unused_addr, args, touch_flag):
    global message
    if touch_flag:
        message = "Six Test Message"

def TouchSeven(unused_addr, args, touch_flag):
    global message
    if touch_flag:
        message = "Seven Test Message"

Screen(1.0, 1.0)

dispatcher = Dispatcher()
dispatcher.map("/avatar/parameters/Touch", Touch, "TouchFlag")
dispatcher.map("/avatar/parameters/TouchOne", TouchOne, "TouchFlag")
dispatcher.map("/avatar/parameters/TouchTwo", TouchTwo, "TouchFlag")
dispatcher.map("/avatar/parameters/TouchThree", TouchThree, "TouchFlag")
dispatcher.map("/avatar/parameters/TouchFour", TouchFour, "TouchFlag")
dispatcher.map("/avatar/parameters/TouchFive", TouchFive, "TouchFlag")
dispatcher.map("/avatar/parameters/TouchSix", TouchSix, "TouchFlag")
dispatcher.map("/avatar/parameters/TouchSeven", TouchSeven, "TouchFlag")
dispatcher.map("/avatar/parameters/Enter", Check, "TouchFlag")
server = osc_server.BlockingOSCUDPServer(
    ('127.0.0.1', 9001), dispatcher)
server.serve_forever()
