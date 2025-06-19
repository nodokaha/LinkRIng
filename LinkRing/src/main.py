# -*- coding: utf-8 -*-
import tweepy
import argparse
import webbrowser
import flet as ft
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
image_count = 1

def SettingImageList():
    global image_count
    CSIDL_MYPICTURES = 0x27
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_MYPICTURES, 0, 0, buf)
    picture_folder = list(Path(buf.value + '/VRChat/' + datetime.now().strftime("%Y-%m")).glob(r'*.png'))
    picture_folder.sort(key=os.path.getctime, reverse=True)
    media_path_list = picture_folder[0:int(image_count)]
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
        client.send_message("/avatar/parameters/Check", 1)
        client.send_message("/avatar/parameters/Check", 0)
        print("check")
        Screen(0.25, 1.0)

def Check(unused_addr, args, touch_flag):
    global message
    if touch_flag:
        print("tweet")
        client.send_message("/avatar/parameters/Check", 1)
        client.send_message("/avatar/parameters/Check", 0)
        TweetPost(message, SettingImageList())
        Screen(0.5, 1.0)

def TouchOne(unused_addr, args, touch_flag):
    global message
    if touch_flag:
        message = message_one

def TouchTwo(unused_addr, args, touch_flag):
    global message
    if touch_flag:
        message = message_two

def TouchThree(unused_addr, args, touch_flag):
    global message
    if touch_flag:
        message = message_three

def TouchFour(unused_addr, args, touch_flag):
    global message
    if touch_flag:
        message = message_four

def TouchFive(unused_addr, args, touch_flag):
    global message
    if touch_flag:
        message = message_five

def TouchSix(unused_addr, args, touch_flag):
    global message
    if touch_flag:
        message = message_six

def TouchSeven(unused_addr, args, touch_flag):
    global message
    if touch_flag:
        message = message_seven

def main(page: ft.Page):
    global image_count
    global api
    global user_at
    global user_ats
    if Path(".token_config").exists():
        f = open(".token_config", "r")
        user_at, user_ats, image_count = json.load(f)
        auth = tweepy.OAuth1UserHandler(at, ats, user_at, user_ats)
        api = tweepy.API(auth)
    else:
        oauth1_user_handler = tweepy.OAuth1UserHandler(
            at, ats,
            callback="oob"
        )
        webbrowser.open(oauth1_user_handler.get_authorization_url(signin_with_twitter=True))
        pw = ft.TextField(label="Input Pin CODE", password=True, can_reveal_password=True)
        def auth(e):        
            user_at, user_ats = oauth1_user_handler.get_access_token(
                pw.value
            )
            f = open(".token_config", "w")
            json.dump([user_at, user_ats, image_count], f)
            auth = tweepy.OAuth1UserHandler(at, ats, user_at, user_ats)
            api = tweepy.API(auth)
            page.controls.pop(0)
            page.update()
        page.add(ft.Row(controls=[pw, ft.ElevatedButton(text="Enter", on_click=auth)]))

    def set_image_count(e):
        global image_count
        image_count = e.control.value
        page.update()

    counter = ft.RadioGroup(content=ft.Column(
    [
        ft.Radio(value=1, label="1枚"),
        ft.Radio(value=2, label="2枚"),
        ft.Radio(value=3, label="3枚"),
        ft.Radio(value=4, label="4枚"),
    ]), on_change=set_image_count, value=image_count)

    def set_message(e):
        global message_one
        global message_two
        global message_three
        global message_four
        global message_five
        global message_six
        global message_seven
        message_one = t1.value
        message_two = t2.value
        message_three = t3.value
        message_four = t4.value
        message_five = t5.value
        message_six = t6.value
        message_seven = t7.value
        page.update()

    t1 = ft.TextField(label="message_one")
    t2 = ft.TextField(label="message_two")
    t3 = ft.TextField(label="message_three")
    t4 = ft.TextField(label="message_four")
    t5 = ft.TextField(label="message_five")
    t6 = ft.TextField(label="message_six")
    t7 = ft.TextField(label="message_seven")
    
    page.add(
        ft.SafeArea(
            ft.Container(
                counter,
                alignment=ft.alignment.center,
            ),
            expand=True,
        ),
        ft.Row(
            controls=[t1, ft.ElevatedButton(text="set", on_click=set_message)]
        ),
        ft.Row(
            controls=[t2, ft.ElevatedButton(text="set", on_click=set_message)]
        ),
        ft.Row(
            controls=[t3, ft.ElevatedButton(text="set", on_click=set_message)]
        ),
        ft.Row(
            controls=[t4, ft.ElevatedButton(text="set", on_click=set_message)]
        ),
        ft.Row(
            controls=[t5, ft.ElevatedButton(text="set", on_click=set_message)]
        ),
        ft.Row(
            controls=[t6, ft.ElevatedButton(text="set", on_click=set_message)]
        ),
        ft.Row(
            controls=[t7, ft.ElevatedButton(text="set", on_click=set_message)]
        )
    )

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

ft.app(main)
