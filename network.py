#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

"""
    Module dedicated to network functions
"""

import time
import datetime
from io import BytesIO
import json
import random
import requests
from imap_tools import MailBox, Q
import pingparsing
from config import Config
import pycurl
import compute


def network_ping(target, count):
    """ ping target """
    result = []
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = target
    transmitter.count = count

    tresult = transmitter.ping()
    json_str = json.dumps(
        ping_parser.parse(tresult).as_dict(), indent=4, separators=(",", ":")
    )
    loaded_json = json.loads(json_str)
    result.append("timestamp: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for i in loaded_json:
        result.append(i + ": " + str(loaded_json[i]))
    return compute.compute_markdown_rendering(2, result)


def network_bonjourmadame(pictype):
    """ Connect to bonjour API (non-official) and get picture to post it. """
    config = Config("config.yaml")
    if config.bonjourmadame_url_api is not None:
        blacklist_pictures = ()
        msg_error_list = ("BonjourMadame API is unhappy :( ", "(B)OOps: ")
        if config.bonjourmadame_blacklist_pics is not None:
            blacklist_pictures = config.bonjourmadame_blacklist_pics
            url = config.bonjourmadame_url_api + pictype
        print("pictype is: " + pictype)
        try:
            wait = 3
            result = requests.get(url, timeout=2).json()["url"]
            if config.bonjourmadame_blacklist_pics is not None:
                while result in blacklist_pictures:
                    print(
                        "found blacklist picture ("
                        + result
                        + "), trying to call another one..."
                    )
                    wait = wait + 1
                    time.sleep(wait)
                    url = config.bonjourmadame_url_api + "random"
                    result = requests.get(url, timeout=2).json()["url"]
            else:
                result = requests.get(url, timeout=2).json()["url"]
            return compute.compute_markdown_rendering(4, result)
        except requests.exceptions.HTTPError as errh:
            result = random.choice(msg_error_list) + str(errh)
            return result
        except requests.exceptions.ConnectionError as errc:
            result = "BonjourMadame is unreachable :( " + str(errc)
            return result
        except requests.exceptions.Timeout as errt:
            result = "BonjourMadame is too slow to respond :( " + str(errt)
            return result
        except requests.exceptions.RequestException as err:
            result = "BonjourMadame (B)OOps: " + str(err)
            return result
    else:
        return "This feature is not configured.Please review your config.yaml."


def network_reach(url, parameters):
    """ Check URL return codes and various troubleshoot informations """
    result = dict()
    body = BytesIO()
    con = pycurl.Curl()
    # c.setopt(pycurl.VERBOSE, True)
    con.setopt(
        pycurl.USERAGENT, "Alfred Pennyworth instance"
    )  # Bypass fortigates WAF default conf 'denied'
    con.setopt(con.URL, url)
    con.setopt(con.TIMEOUT, 5)
    con.setopt(
        con.WRITEDATA, body
    )  # todo: !c reach xxx.com details and send the buffer stack
    con.setopt(con.FOLLOWLOCATION, True)
    try:
        con.perform()
        result["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        result["url-target"] = con.getinfo(con.EFFECTIVE_URL)
        result["http-return-code"] = con.getinfo(con.RESPONSE_CODE)
        result["namelookup-time"] = con.getinfo(con.NAMELOOKUP_TIME)
        # TCP/IP 3-way handshaking time
        result["connect-time"] = con.getinfo(con.CONNECT_TIME)
        # time-to-first-byte time
        result["Time-To-First-Byte"] = con.getinfo(con.STARTTRANSFER_TIME)
        result["total-time"] = con.getinfo(con.TOTAL_TIME)  # last query time
        result["redirect-count"] = con.getinfo(con.REDIRECT_COUNT)
        result["cert-health-(1=KO)"] = con.getinfo(con.SSL_VERIFYRESULT)
        con.close()
        if parameters == "details":
            result["DETAILS"] = body.getvalue()
        return compute.compute_markdown_rendering(3, result)
    except pycurl.error:
        return str("Error :( =>" + str(pycurl.error))


def network_mailbox(action):
    """ Fetch mail box with stats and latest 10 mails dates/subjects"""
    config = Config("config.yaml")
    result = dict()
    if action in ("clear", "clearall"):
        with MailBox(config.mailbox_host).login(
            config.mailbox_username,
            config.mailbox_password,
            initial_folder=config.mailbox_folder,
        ) as mailbox:
            mailbox.delete([msg.uid for msg in mailbox.fetch()])
            return (
                "mailbox "
                + config.mailbox_name
                + " ("
                + config.mailbox_folder
                + ")"
                + " has been cleared !"
            )
    if action == "get":
        with MailBox(config.mailbox_host).login(
            config.mailbox_username,
            config.mailbox_password,
            initial_folder=config.mailbox_folder,
        ) as mailbox:
            msgcount = 0
            for msg in mailbox.fetch(Q(date=datetime.date.today()), reverse=True):
                print(msg)
                msgcount = msgcount + 1
            for msg in mailbox.fetch(
                Q(date=datetime.date.today()), limit=10, reverse=True
            ):
                result[str(msg.date)] = msg.subject
                if msgcount > 0:
                    result["!!! "] = (str(msgcount) + " mail have been found in the mailbox !!!")
                return compute.compute_markdown_rendering(3, result)
            else:
                return (
                    ":):):) 0 mails in mailbox "
                    + config.mailbox_name
                    + " ("
                    + config.mailbox_folder
                    + ")"
                )
