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
client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
message = "test Message"
image_count = 1
ohatweet = False


def SettingImageList():
    global image_count
    CSIDL_MYPICTURES = 0x27
    buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_MYPICTURES, 0, 0, buf)
    picture_folder = list(
        Path(buf.value + "/VRChat/" + datetime.now().strftime("%Y-%m")).glob(r"*.png")
    )
    picture_folder.sort(key=os.path.getctime, reverse=True)
    media_path_list = picture_folder[0 : int(image_count)]
    media_list = []
    Screen(0.25, 1)
    for x in media_path_list:
        img = api.media_upload(x.resolve())
        media_list += [img.media_id]
        print(x.resolve())
    return media_list


def TweetPost(message, media_list):
    client = tweepy.Client(
        consumer_key=at,
        consumer_secret=ats,
        access_token=user_at,
        access_token_secret=user_ats,
    )
    client.create_tweet(text=message, media_ids=media_list)
    Screen(0.5, 1)
    print("tweet media")


def Screen(x, y):
    client.send_message("/avatar/parameters/ScreenX", x)
    client.send_message("/avatar/parameters/ScreenY", y)


def Touch(unused_addr, args, touch_flag):
    if touch_flag:
        client.send_message("/avatar/parameters/Check", 1)
        print("check")
        Screen(0.25, 1.0)


def Check(unused_addr, args, touch_flag):
    global message
    if touch_flag:
        print("tweet")
        client.send_message("/avatar/parameters/Check", 0)
        if ohatweet:
            match datetime.weekday():
                case 0:
                    message = message_one
                case 1:
                    message = message_two
                case 2:
                    message = message_three
                case 3:
                    message = message_four
                case 4:
                    message = message_five
                case 5:
                    message = message_six
                case 6:
                    message = message_seven
        TweetPost(message, SettingImageList())
        Screen(0.5, 1.0)


def TouchOne(unused_addr, args, touch_flag):
    global message
    print("touch one")
    if touch_flag:
        message = message_one


def TouchTwo(unused_addr, args, touch_flag):
    global message
    print("touch two")
    if touch_flag:
        message = message_two


def TouchThree(unused_addr, args, touch_flag):
    global message
    print("touch three")
    if touch_flag:
        message = message_three


def TouchFour(unused_addr, args, touch_flag):
    global message
    print("touch four")
    if touch_flag:
        message = message_four


def TouchFive(unused_addr, args, touch_flag):
    global message
    print("touch five")
    if touch_flag:
        message = message_five


def TouchSix(unused_addr, args, touch_flag):
    global message
    print("touch six")
    if touch_flag:
        message = message_six


def TouchSeven(unused_addr, args, touch_flag):
    global message
    print("touch seven")
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
        print("load success")
    else:
        oauth1_user_handler = tweepy.OAuth1UserHandler(at, ats, callback="oob")
        webbrowser.open(
            oauth1_user_handler.get_authorization_url(signin_with_twitter=True)
        )
        print("auth")
        pw = ft.TextField(
            label="Input Pin CODE", password=True, can_reveal_password=True
        )

        def auth(e):
            user_at, user_ats = oauth1_user_handler.get_access_token(pw.value)
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
        print(image_count)
        page.update()

    counter = ft.RadioGroup(
        content=ft.Column(
            [
                ft.Radio(value=1, label="1枚"),
                ft.Radio(value=2, label="2枚"),
                ft.Radio(value=3, label="3枚"),
                ft.Radio(value=4, label="4枚"),
            ]
        ),
        on_change=set_image_count,
        value=image_count,
    )

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

    t1 = ft.TextField()
    t2 = ft.TextField()
    t3 = ft.TextField()
    t4 = ft.TextField()
    t5 = ft.TextField()
    t6 = ft.TextField()
    t7 = ft.TextField()

    t1_label = ft.Text(value=("message_one" if not ohatweet else "月曜日"))
    t2_label = ft.Text(value=("message_two" if not ohatweet else "火曜日"))
    t3_label = ft.Text(value=("message_three" if not ohatweet else "水曜日"))
    t4_label = ft.Text(value=("message_four" if not ohatweet else "木曜日"))
    t5_label = ft.Text(value=("message_five" if not ohatweet else "金曜日"))
    t6_label = ft.Text(value=("message_six" if not ohatweet else "土曜日"))
    t7_label = ft.Text(value=("message_seven" if not ohatweet else "日曜日"))

    def set_ohatweet(e):
        global ohatweet
        ohatweet = not ohatweet
        print("おはツイモード: ", ohatweet)
        t1_label.value = "message_one" if not ohatweet else "月曜日"
        t2_label.value = "message_two" if not ohatweet else "火曜日"
        t3_label.value = "message_three" if not ohatweet else "水曜日"
        t4_label.value = "message_four" if not ohatweet else "木曜日"
        t5_label.value = "message_five" if not ohatweet else "金曜日"
        t6_label.value = "message_six" if not ohatweet else "土曜日"
        t7_label.value = "message_seven" if not ohatweet else "日曜日"
        page.update()

    page.add(
        ft.Row(
            [
                ft.Column(
                    [
                        ft.Switch(
                            label="おはツイモード",
                            value=ohatweet,
                            on_change=set_ohatweet,
                        ),
                        t1_label,
                        ft.Row(
                            controls=[
                                t1,
                                ft.ElevatedButton(text="set", on_click=set_message),
                            ]
                        ),
                        t2_label,
                        ft.Row(
                            controls=[
                                t2,
                                ft.ElevatedButton(text="set", on_click=set_message),
                            ]
                        ),
                        t3_label,
                        ft.Row(
                            controls=[
                                t3,
                                ft.ElevatedButton(text="set", on_click=set_message),
                            ]
                        ),
                        t4_label,
                        ft.Row(
                            controls=[
                                t4,
                                ft.ElevatedButton(text="set", on_click=set_message),
                            ]
                        ),
                        t5_label,
                        ft.Row(
                            controls=[
                                t5,
                                ft.ElevatedButton(text="set", on_click=set_message),
                            ]
                        ),
                        t6_label,
                        ft.Row(
                            controls=[
                                t6,
                                ft.ElevatedButton(text="set", on_click=set_message),
                            ]
                        ),
                        t7_label,
                        ft.Row(
                            controls=[
                                t7,
                                ft.ElevatedButton(text="set", on_click=set_message),
                            ]
                        ),
                    ]
                ),
                ft.Text(value="投稿枚数"),
                ft.SafeArea(
                    ft.Container(
                        counter,
                        alignment=ft.alignment.center,
                    ),
                    expand=True,
                ),
            ]
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
    server = osc_server.BlockingOSCUDPServer(("127.0.0.1", 9001), dispatcher)
    server.serve_forever()


ft.app(main)
