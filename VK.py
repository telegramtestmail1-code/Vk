# ⚠️ DISCLAIMER: This bot is provided for entertainment and educational purposes only.
# The developer does not endorse or encourage any harmful, abusive, or illegal activities.
# Use this software responsibly and in compliance with Telegram's Terms of Service.
#
# 🔐 IMPORTANT: The bot token in this code is exposed. If you have shared this file
# publicly, revoke the token immediately via @BotFather and replace it with a new one.

import asyncio
import logging
import random
import io
import os
import sys
import subprocess
import json
from typing import Optional, Dict, Set, List

from telegram import Update, constants, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes, MessageHandler, filters, CommandHandler, CallbackQueryHandler
from telegram.error import BadRequest, RetryAfter

# ==================== CONFIGURATION ====================
OWNER_ID = 5703874798
DEVELOPER_NAME = "Cʟɪᴄᴋ Hᴇʀᴇ !!"
DEVELOPER_LINK = f"[{DEVELOPER_NAME}](tg://openmessage?user_id={OWNER_ID})"
BOT_TOKEN = "8612619822:AAFIuv-VfEQCA8bxnokj6w_7tAeRMK-vee0"
MAIN_BOT_USERNAME = "ZSexsBot"
DATA_FILE = "bot_data.json"
CLONED_BOTS_FILE = "cloned_bots.json"

# ==================== REQUIRED CHANNEL/GROUP ====================
REQUIRED_CHAT = "@ZcuzSuppports"  # Set to "" to disable force-join (used for clones)

# ==================== PROTECTED GROUPS ====================
GROUP = []

# ==================== MESSAGE LISTS (EMPTY – YOU FILL THEM) ====================
# ©
RAID_MESSAGES= [
    "𝗠𝗔̂𝗔̂𝗗𝗔𝗥𝗖𝗛Ø𝗗 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘 𝗚𝗛𝗨𝗧𝗞𝗔 𝗞𝗛𝗔𝗔𝗞𝗘 𝗧𝗛𝗢𝗢𝗞 𝗗𝗨𝗡𝗚𝗔 🤣🤣",
    "𝗧𝗘𝗥𝗘 𝗕𝗘́𝗛𝗘𝗡 𝗞 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘 𝗖𝗛𝗔𝗞𝗨 𝗗𝗔𝗔𝗟 𝗞𝗔𝗥 𝗖𝗛𝗨𝗨́𝗧 𝗞𝗔 𝗞𝗛𝗢𝗢𝗡 𝗞𝗔𝗥 𝗗𝗨𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗩𝗔𝗛𝗘𝗘𝗡 𝗡𝗛𝗜 𝗛𝗔𝗜 𝗞𝗬𝗔? 9 𝗠𝗔𝗛𝗜𝗡𝗘 𝗥𝗨𝗞 𝗦𝗔𝗚𝗜 𝗩𝗔𝗛𝗘𝗘𝗡 𝗗𝗘𝗧𝗔 𝗛𝗨 🤣🤣🤩",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞 𝗕𝗛𝗢𝗦𝗗𝗘 𝗠𝗘 𝗔𝗘𝗥𝗢𝗣𝗟𝗔𝗡𝗘𝗣𝗔𝗥𝗞 𝗞𝗔𝗥𝗞𝗘 𝗨𝗗𝗔𝗔𝗡 𝗕𝗛𝗔𝗥 𝗗𝗨𝗚𝗔 ✈️🛫",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘 𝗦𝗨𝗧𝗟𝗜 𝗕𝗢𝗠𝗕 𝗙𝗢𝗗 𝗗𝗨𝗡𝗚𝗔 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗝𝗛𝗔𝗔𝗧𝗘 𝗝𝗔𝗟 𝗞𝗘 𝗞𝗛𝗔𝗔𝗞 𝗛𝗢 𝗝𝗔𝗬𝗘𝗚𝗜💣",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘 𝗦𝗖𝗢𝗢𝗧𝗘𝗥 𝗗𝗔𝗔𝗟 𝗗𝗨𝗚𝗔👅",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗞𝗔𝗞𝗧𝗘 🤱 𝗚𝗔𝗟𝗜 𝗞𝗘 𝗞𝗨𝗧𝗧𝗢 🦮 𝗠𝗘 𝗕𝗔𝗔𝗧 𝗗𝗨𝗡𝗚𝗔 𝗣𝗛𝗜𝗥 🍞 𝗕𝗥𝗘𝗔𝗗 𝗞𝗜 𝗧𝗔𝗥𝗛 𝗞𝗛𝗔𝗬𝗘𝗡𝗚𝗘 𝗪𝗢 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧",
    "𝗗𝗨𝗗𝗛 𝗛𝗜𝗟𝗔𝗔𝗨𝗡𝗚𝗔 𝗧𝗘𝗥𝗜 𝗩𝗔𝗛𝗘𝗘𝗡 𝗞𝗘 𝗨𝗣𝗥 𝗡𝗜𝗖𝗛𝗘 🆙🆒😙",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘 𝐵��������������������������������𝗞𝗔 𝗟𝗨𝗡𝗗 𝗗𝗔𝗟 𝗗𝗨𝗡𝗚𝗔 𝗙𝗜𝗥 𝗢 𝗣𝗥𝗘𝗚𝗡𝗘𝗡𝗧 𝗛𝗢 𝗝𝗔𝗬𝗘𝗚𝗜 🍌🍌😍",
    "𝗧𝗘𝗥𝗜 𝗩𝗔𝗛𝗘𝗘𝗡 𝗗𝗛𝗔𝗡𝗗𝗛𝗘 𝗩𝗔𝗔𝗟𝗜 😋😛",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗘 𝗕𝗛𝗢𝗦𝗗𝗘 𝗠𝗘 𝗔𝗖 𝗟𝗔𝗚𝗔 𝗗𝗨𝗡𝗚𝗔 𝗦𝗔𝗔𝗥𝗜 𝗚𝗔𝗥𝗠𝗜 𝗡𝗜𝗞𝗔𝗟 𝗝𝗔𝗔𝗬𝗘𝗚𝗜",
    "𝗧𝗘𝗥𝗜 𝗩𝗔𝗛𝗘𝗘𝗡 𝗞𝗢 𝗛𝗢𝗥𝗟𝗜𝗖𝗞𝗦 𝗣𝗘𝗘𝗟𝗔𝗨𝗡𝗚𝗔 𝗠𝗔̂𝗔̂𝗗𝗔𝗥𝗖𝗛Ø𝗗😚",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗢 𝗞𝗢𝗟𝗞𝗔𝗧𝗔 𝗩𝗔𝗔𝗟𝗘 𝗝𝗜𝗧𝗨 𝗕𝗛𝗔𝗜𝗬𝗔 𝗞𝗔 𝗟𝗨𝗡𝗗 𝗠𝗨𝗕𝗔𝗥𝗔𝗞 🤩🤩",
    "𝗧𝗘𝗥𝗜 𝗠𝗨𝗠𝗠𝗬 𝗞𝗜 𝗙𝗔𝗡𝗧𝗔𝗦𝗬 𝗛𝗨 𝗟𝗔𝗪𝗗𝗘, 𝗧𝗨 𝗔𝗣𝗡𝗜 𝗕𝗛𝗘𝗡 𝗞𝗢 𝗦𝗠𝗕𝗛𝗔𝗔𝗟 😈😈",
    "𝗧𝗘𝗥𝗔 𝗣𝗘𝗛𝗟𝗔 𝗕𝗔𝗔𝗣 𝗛𝗨 𝗠𝗔̂𝗔̂𝗗𝗔𝗥𝗖𝗛Ø𝗗 ",
    "𝗧𝗘𝗥𝗜 𝗩𝗔𝗛𝗘𝗘𝗡 𝗞𝗘 𝗕𝗛𝗢𝗦𝗗𝗘 𝗠𝗘 𝗫𝗩𝗜𝗗𝗘𝗢𝗦.𝗖𝗢𝗠 𝗖𝗛𝗔𝗟𝗔 𝗞𝗘 𝗠𝗨𝗧𝗛 𝗠𝗔́𝗔̀𝗥𝗨𝗡𝗚𝗔 🤡😹",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗔 𝗚𝗥𝗢𝗨𝗣 𝗩𝗔𝗔𝗟𝗢𝗡 𝗦𝗔𝗔𝗧𝗛 𝗠𝗜𝗟𝗞𝗘 𝗚𝗔𝗡𝗚 𝗕𝗔𝗡𝗚 𝗞𝗥𝗨𝗡𝗚𝗔🙌🏻☠️ ",
    "𝗧𝗘𝗥𝗜 𝗜𝗧𝗘𝗠 𝗞𝗜 𝗚𝗔𝗔𝗡𝗗 𝗠𝗘 𝗟𝗨𝗡𝗗 𝗗𝗔𝗔𝗟𝗞𝗘,𝗧𝗘𝗥𝗘 𝗝𝗔𝗜𝗦𝗔 𝗘𝗞 𝗢𝗥 𝗡𝗜𝗞𝗔𝗔𝗟 𝗗𝗨𝗡𝗚𝗔 𝗠𝗔̂𝗔̂𝗗𝗔𝗥𝗖𝗛Ø𝗗🤘🏻🙌🏻☠️ ",
    "𝗔𝗨𝗞𝗔𝗔𝗧 𝗠𝗘 𝗥𝗘𝗛 𝗩𝗥𝗡𝗔 𝗚𝗔𝗔𝗡𝗗 𝗠𝗘 𝗗𝗔𝗡𝗗𝗔 𝗗𝗔𝗔𝗟 𝗞𝗘 𝗠𝗨𝗛 𝗦𝗘 𝗡𝗜𝗞𝗔𝗔𝗟 𝗗𝗨𝗡𝗚𝗔 𝗦𝗛𝗔𝗥𝗜𝗥 𝗕𝗛𝗜 𝗗𝗔𝗡𝗗𝗘 𝗝𝗘𝗦𝗔 𝗗𝗜𝗞𝗛𝗘𝗚𝗔 🙄🤭🤭",
    "𝗧𝗘𝗥𝗜 𝗠𝗨𝗠𝗠𝗬 𝗞𝗘 𝗦𝗔𝗔𝗧𝗛 𝗟𝗨𝗗𝗢 𝗞𝗛𝗘𝗟𝗧𝗘 𝗞𝗛𝗘𝗟𝗧𝗘 𝗨𝗦𝗞𝗘 𝗠𝗨𝗛 𝗠𝗘 𝗔𝗣𝗡𝗔 𝗟𝗢𝗗𝗔 𝗗𝗘 𝗗𝗨𝗡𝗚𝗔☝🏻☝🏻😬",
    "𝗧𝗘𝗥𝗜 𝗩𝗔𝗛𝗘𝗘𝗡 𝗞𝗢 𝗔𝗣𝗡𝗘 𝗟𝗨𝗡𝗗 𝗣𝗥 𝗜𝗧𝗡𝗔 𝗝𝗛𝗨𝗟𝗔𝗔𝗨𝗡𝗚𝗔 𝗞𝗜 𝗝𝗛𝗨𝗟𝗧𝗘 𝗝𝗛𝗨𝗟𝗧𝗘 𝗛𝗜 𝗕𝗔𝗖𝗛𝗔 𝗣𝗔𝗜𝗗𝗔 𝗞𝗥 𝗗𝗘𝗚𝗜👀👯 ",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗕𝗔𝗧𝗧𝗘𝗥𝗬 𝗟𝗔𝗚𝗔 𝗞𝗘 𝗣𝗢𝗪𝗘𝗥𝗕𝗔𝗡𝗞 𝗕𝗔𝗡𝗔 𝗗𝗨𝗡𝗚𝗔 🔋 🔥🤩",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗖++ 𝗦𝗧𝗥𝗜𝗡𝗚 𝗘𝗡𝗖𝗥𝗬𝗣𝗧𝗜𝗢𝗡 𝗟𝗔𝗚𝗔 𝗗𝗨𝗡𝗚𝗔 𝗕𝗔𝗛𝗧𝗜 𝗛𝗨𝗬𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗥𝗨𝗞 𝗝𝗔𝗬𝗘𝗚𝗜𝗜𝗜𝗜😈🔥😍",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗘 𝗚𝗔𝗔𝗡𝗗 𝗠𝗘𝗜 𝗝𝗛𝗔𝗔𝗗𝗨 𝗗𝗔𝗟 𝗞𝗘 𝗠𝗢𝗥 🦚 𝗕𝗔𝗡𝗔 𝗗𝗨𝗡𝗚𝗔𝗔 🤩🥵😱",
    "𝗧𝗘𝗥𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗦𝗛𝗢𝗨𝗟𝗗𝗘𝗥𝗜𝗡𝗚 𝗞𝗔𝗥 𝗗𝗨𝗡𝗚𝗔𝗔 𝗛𝗜𝗟𝗔𝗧𝗘 𝗛𝗨𝗬𝗘 𝗕𝗛𝗜 𝗗𝗔𝗥𝗗 𝗛𝗢𝗚𝗔𝗔𝗔😱🤮👺",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗢 𝗥𝗘𝗗𝗜 𝗣𝗘 𝗕𝗔𝗜𝗧𝗛𝗔𝗟 𝗞𝗘 𝗨𝗦𝗦𝗘 𝗨𝗦𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗕𝗜𝗟𝗪𝗔𝗨𝗡𝗚𝗔𝗔 💰 😵🤩",
    "𝗕𝗛𝗢𝗦𝗗𝗜𝗞𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 4 𝗛𝗢𝗟𝗘 𝗛𝗔𝗜 𝗨𝗡𝗠𝗘 𝗠𝗦𝗘𝗔𝗟 𝗟𝗔𝗚𝗔 𝗕𝗔𝗛𝗨𝗧 𝗕𝗔𝗛𝗘𝗧𝗜 𝗛𝗔𝗜 𝗕𝗛𝗢𝗙𝗗𝗜𝗞𝗘👊🤮🤢🤢",
    "𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗕𝗔𝗥𝗚𝗔𝗗 𝗞𝗔 𝗣𝗘𝗗 𝗨𝗚𝗔 𝗗𝗨𝗡𝗚𝗔𝗔 𝗖𝗢𝗥𝗢𝗡𝗔 𝗠𝗘𝗜 𝗦𝗔𝗕 𝗢𝗫𝗬𝗚𝗘𝗡 𝗟𝗘𝗞𝗔𝗥 𝗝𝗔𝗬𝗘𝗡𝗚𝗘🤢🤩🥳",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗦𝗨𝗗𝗢 𝗟𝗔𝗚𝗔 𝗞𝗘 𝗕𝗜𝗚𝗦𝗣𝗔𝗠 𝗟𝗔𝗚𝗔 𝗞𝗘 9999 𝗙𝗨𝗖𝗞 𝗟𝗔𝗚𝗔𝗔 𝗗𝗨 🤩🥳🔥",
    "𝗧𝗘𝗥𝗜 𝗩𝗔𝗛𝗘𝗡 𝗞𝗘 𝗕𝗛𝗢𝗦𝗗𝗜𝗞𝗘 𝗠𝗘𝗜 𝗕𝗘𝗦𝗔𝗡 𝗞𝗘 𝗟𝗔𝗗𝗗𝗨 𝗕𝗛𝗔𝗥 𝗗𝗨𝗡𝗚𝗔🤩🥳🔥😈",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗞𝗛𝗢𝗗 𝗞𝗘 𝗨𝗦𝗠𝗘 𝗖𝗬𝗟𝗜𝗡𝗗𝗘𝗥 ⛽️ 𝗙𝗜𝗧 𝗞𝗔𝗥𝗞𝗘 𝗨𝗦𝗠𝗘𝗘 𝗗𝗔𝗟 𝗠𝗔𝗞𝗛𝗔𝗡𝗜 𝗕𝗔𝗡𝗔𝗨𝗡𝗚𝗔𝗔𝗔🤩👊🔥",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗦𝗛𝗘𝗘𝗦𝗛𝗔 𝗗𝗔𝗟 𝗗𝗨𝗡𝗚𝗔𝗔𝗔 𝗔𝗨𝗥 𝗖𝗛𝗔𝗨𝗥𝗔𝗛𝗘 𝗣𝗘 𝗧𝗔𝗔𝗡𝗚 𝗗𝗨𝗡𝗚𝗔 𝗕𝗛𝗢𝗦𝗗𝗜𝗞𝗘😈😱🤩",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗖𝗥𝗘𝗗𝗜𝗧 𝗖𝗔𝗥𝗗 𝗗𝗔𝗟 𝗞𝗘 𝗔𝗚𝗘 𝗦𝗘 500 𝗞𝗘 𝗞𝗔𝗔𝗥𝗘 𝗞𝗔𝗔𝗥𝗘 𝗡𝗢𝗧𝗘 𝗡𝗜𝗞𝗔𝗟𝗨𝗡𝗚𝗔𝗔 𝗕𝗛𝗢𝗦𝗗𝗜𝗞𝗘💰💰🤩",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗘 𝗦𝗔𝗧𝗛 𝗦𝗨𝗔𝗥 𝗞𝗔 𝗦𝗘𝗫 𝗞𝗔𝗥𝗪𝗔 𝗗𝗨𝗡𝗚𝗔𝗔 𝗘𝗞 𝗦𝗔𝗧𝗛 6-6 𝗕𝗔𝗖𝗛𝗘 𝗗𝗘𝗚𝗜💰🔥😱",
    "𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗔𝗣𝗣𝗟𝗘 𝗞𝗔 18𝗪 𝗪𝗔𝗟𝗔 𝗖𝗛𝗔𝗥𝗚𝗘𝗥 🔥🤩",
    "𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗜 𝗚𝗔𝗔𝗡𝗗 𝗠𝗘𝗜 𝗢𝗡𝗘𝗣𝗟𝗨𝗦 𝗞𝗔 𝗪𝗥𝗔𝗣 𝗖𝗛𝗔𝗥𝗚𝗘𝗥 30𝗪 𝗛𝗜𝗚𝗛 𝗣𝗢𝗪𝗘𝗥 💥😂😎",
    "𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗞𝗢 𝗔𝗠𝗔𝗭𝗢𝗡 𝗦𝗘 𝗢𝗥𝗗𝗘𝗥 𝗞𝗔𝗥𝗨𝗡𝗚𝗔 10 𝗿𝘀 𝗠𝗘𝗜 𝗔𝗨𝗥 𝗙𝗟𝗜𝗣𝗞𝗔𝗥𝗧 𝗣𝗘 20 𝗥𝗦 𝗠𝗘𝗜 𝗕𝗘𝗖𝗛 𝗗𝗨𝗡𝗚𝗔🤮👿😈🤖",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗕𝗔𝗗𝗜 𝗕𝗛𝗨𝗡𝗗 𝗠𝗘 𝗭𝗢𝗠𝗔𝗧𝗢 𝗗𝗔𝗟 𝗞𝗘 𝗦𝗨𝗕𝗪𝗔𝗬 𝗞𝗔 𝗕𝗙𝗙 𝗩𝗘𝗚 𝗦𝗨𝗕 𝗖𝗢𝗠𝗕𝗢 [15𝗰𝗺 , 16 𝗶𝗻𝗰𝗵𝗲𝘀 ] 𝗢𝗥𝗗𝗘𝗥 𝗖𝗢𝗗 𝗞𝗥𝗩𝗔𝗨𝗡𝗚𝗔 𝗢𝗥 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗝𝗔𝗕 𝗗𝗜𝗟𝗜𝗩𝗘𝗥𝗬 𝗗𝗘𝗡𝗘 𝗔𝗬𝗘𝗚𝗜 𝗧𝗔𝗕 𝗨𝗦𝗣𝗘 𝗝𝗔𝗔𝗗𝗨 𝗞𝗥𝗨𝗡𝗚𝗔 𝗢𝗥 𝗙𝗜𝗥 9 𝗠𝗢𝗡𝗧𝗛 𝗕𝗔𝗔𝗗 𝗩𝗢 𝗘𝗞 𝗢𝗥 𝗙𝗥𝗘𝗘 𝗗𝗜𝗟𝗜𝗩𝗘𝗥𝗬 𝗗𝗘𝗚𝗜🙀👍🥳🔥",
    "𝗧𝗘𝗥𝗜 𝗕𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗞𝗔𝗔𝗟𝗜🙁🤣💥",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘 𝗖𝗛𝗔𝗡𝗚𝗘𝗦 𝗖𝗢𝗠𝗠𝗜𝗧 𝗞𝗥𝗨𝗚𝗔 𝗙𝗜𝗥 𝗧𝗘𝗥𝗜 𝗕𝗛𝗘𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗔𝗨𝗧𝗢𝗠𝗔𝗧𝗜𝗖𝗔𝗟𝗟𝗬 𝗨𝗣𝗗𝗔𝗧𝗘 𝗛𝗢𝗝𝗔𝗔𝗬𝗘𝗚𝗜🤖🙏🤔",
    "𝗧𝗘𝗥𝗜 𝗠𝗔𝗨𝗦𝗜 𝗞𝗘 𝗕𝗛𝗢𝗦𝗗𝗘 𝗠𝗘𝗜 𝗜𝗡𝗗𝗜𝗔𝗡 𝗥𝗔𝗜𝗟𝗪𝗔𝗬 🚂💥😂",
    "𝗧𝗨 𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗧𝗘𝗥𝗔 𝗞𝗛𝗔𝗡𝗗𝗔𝗡 𝗦𝗔𝗕 𝗕𝗔𝗛𝗘𝗡 𝗞𝗘 𝗟𝗔𝗪𝗗𝗘 𝗥Æ𝗡𝗗𝗜 𝗛𝗔𝗜 𝗥Æ𝗡𝗗𝗜 🤢✅🔥",
    "𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗜𝗢𝗡𝗜𝗖 𝗕𝗢𝗡𝗗 𝗕𝗔𝗡𝗔 𝗞𝗘 𝗩𝗜𝗥𝗚𝗜𝗡𝗜𝗧𝗬 𝗟𝗢𝗢𝗦𝗘 𝗞𝗔𝗥𝗪𝗔 𝗗𝗨𝗡𝗚𝗔 𝗨𝗦𝗞𝗜 📚 😎🤩",
    "𝗧𝗘𝗥𝗜 𝗥Æ𝗡𝗗𝗜 𝗠𝗔́𝗔̀ 𝗦𝗘 𝗣𝗨𝗖𝗛𝗡𝗔 𝗕𝗔𝗔𝗣 𝗞𝗔 𝗡𝗔𝗔𝗠 𝗕𝗔𝗛𝗘𝗡 𝗞𝗘 𝗟𝗢𝗗𝗘𝗘𝗘𝗘𝗘 🤩🥳😳",
    "𝗧𝗨 𝗔𝗨𝗥 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗗𝗢𝗡𝗢 𝗞𝗜 𝗕𝗛𝗢𝗦𝗗𝗘 𝗠𝗘𝗜 𝗠𝗘𝗧𝗥𝗢 𝗖𝗛𝗔𝗟𝗪𝗔 𝗗𝗨𝗡𝗚𝗔 𝗠𝗔𝗗𝗔𝗥𝗫𝗛𝗢𝗗 🚇🤩😱🥶",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗢 𝗜𝗧𝗡𝗔 𝗖𝗛𝗢𝗗𝗨𝗡𝗚𝗔 𝗧𝗘𝗥𝗔 𝗕𝗔𝗔𝗣 𝗕𝗛𝗜 𝗨𝗦𝗞𝗢 𝗣𝗔𝗛𝗖𝗛𝗔𝗡𝗔𝗡𝗘 𝗦𝗘 𝗠𝗔𝗡𝗔 𝗞𝗔𝗥 𝗗𝗘𝗚𝗔😂👿🤩",
    "𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗘 𝗕𝗛𝗢𝗦𝗗𝗘 𝗠𝗘𝗜 𝗛𝗔𝗜𝗥 𝗗𝗥𝗬𝗘𝗥 𝗖𝗛𝗔𝗟𝗔 𝗗𝗨𝗡𝗚𝗔𝗔💥🔥🔥",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗧𝗘𝗟𝗘𝗚𝗥𝗔𝗠 𝗞𝗜 𝗦𝗔𝗥𝗜 𝗥Æ𝗡𝗗𝗜𝗬𝗢𝗡 𝗞𝗔 𝗥Æ𝗡𝗗𝗜 𝗞𝗛𝗔𝗡𝗔 𝗞𝗛𝗢𝗟 𝗗𝗨𝗡𝗚𝗔𝗔👿🤮😎",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗔𝗟𝗘𝗫𝗔 𝗗𝗔𝗟 𝗞𝗘𝗘 𝗗𝗝 𝗕𝗔𝗝𝗔𝗨𝗡𝗚𝗔𝗔𝗔 🎶 ⬆️🤩💥",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗘 𝗕𝗛𝗢𝗦𝗗𝗘 𝗠𝗘𝗜 𝗚𝗜𝗧𝗛𝗨𝗕 𝗗𝗔𝗟 𝗞𝗘 𝗔𝗣𝗡𝗔 𝗕𝗢𝗧 𝗛𝗢𝗦𝗧 𝗞𝗔𝗥𝗨𝗡𝗚𝗔𝗔 🤩👊👤😍",
    "𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗔 𝗩𝗣𝗦 𝗕𝗔𝗡𝗔 𝗞𝗘 24*7 𝗕𝗔𝗦𝗛 𝗖𝗛𝗨𝗗𝗔𝗜 𝗖𝗢𝗠𝗠𝗔𝗡𝗗 𝗗𝗘 𝗗𝗨𝗡𝗚𝗔𝗔 🤩💥🔥🔥",
    "𝗧𝗘𝗥𝗜 𝗠𝗨𝗠𝗠𝗬 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗧𝗘𝗥𝗘 𝗟𝗔𝗡𝗗 𝗞𝗢 𝗗𝗔𝗟 𝗞𝗘 𝗞𝗔𝗔𝗧 𝗗𝗨𝗡𝗚𝗔 𝗠𝗔̂𝗔̂𝗗𝗔𝗥𝗖𝗛Ø𝗗 🔪😂🔥",
    "𝗦𝗨𝗡 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗔 𝗕𝗛𝗢𝗦𝗗𝗔 𝗔𝗨𝗥 𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗔 𝗕𝗛𝗜 𝗕𝗛𝗢𝗦𝗗𝗔 👿😎👊",
    "𝗧𝗨𝗝𝗛𝗘 𝗗𝗘𝗞𝗛 𝗞𝗘 𝗧𝗘𝗥𝗜 𝗥Æ𝗡𝗗𝗜 𝗕𝗔𝗛𝗘𝗡 𝗣𝗘 𝗧𝗔𝗥𝗔𝗦 𝗔𝗧𝗔 𝗛𝗔𝗜 𝗠𝗨𝗝𝗛𝗘 𝗕𝗔𝗛𝗘𝗡 𝗞𝗘 𝗟𝗢𝗗𝗘𝗘𝗘𝗘 👿💥🤩🔥",
    "𝗦𝗨𝗡 𝗠𝗔̂𝗔̂𝗗𝗔𝗥𝗖𝗛Ø𝗗 𝗝𝗬𝗔𝗗𝗔 𝗡𝗔 𝗨𝗖𝗛𝗔𝗟 𝗠𝗔́𝗔̀ 𝗖𝗛𝗢𝗗 𝗗𝗘𝗡𝗚𝗘 𝗘𝗞 𝗠𝗜𝗡 𝗠𝗘𝗜 ✅🤣🔥🤩",
    "𝗔𝗣𝗡𝗜 𝗔𝗠𝗠𝗔 𝗦𝗘 𝗣𝗨𝗖𝗛𝗡𝗔 𝗨𝗦𝗞𝗢 𝗨𝗦 𝗞𝗔𝗔𝗟𝗜 𝗥𝗔𝗔𝗧 𝗠𝗘𝗜 𝗞𝗔𝗨𝗡 𝗖𝗛𝗢𝗗𝗡𝗘𝗘 𝗔𝗬𝗔 𝗧𝗛𝗔𝗔𝗔! 𝗧𝗘𝗥𝗘 𝗜𝗦 𝗣𝗔𝗣𝗔 𝗞𝗔 𝗡𝗔𝗔𝗠 𝗟𝗘𝗚𝗜 😂👿😳",
    "𝗧𝗢𝗛𝗔𝗥 𝗕𝗔𝗛𝗜𝗡 𝗖𝗛𝗢𝗗𝗨 𝗕𝗕𝗔𝗛𝗘𝗡 𝗞𝗘 𝗟𝗔𝗪𝗗𝗘 𝗨𝗦𝗠𝗘 𝗠𝗜𝗧𝗧𝗜 𝗗𝗔𝗟 𝗞𝗘 𝗖𝗘𝗠𝗘𝗡𝗧 𝗦𝗘 𝗕𝗛𝗔𝗥 𝗗𝗨 🏠🤢🤩💥",
    "𝗧𝗨𝗝𝗛𝗘 𝗔𝗕 𝗧𝗔𝗞 𝗡𝗔𝗛𝗜 𝗦𝗠𝗝𝗛 𝗔𝗬𝗔 𝗞𝗜 𝗠𝗔𝗜 𝗛𝗜 𝗛𝗨 𝗧𝗨𝗝𝗛𝗘 𝗣𝗔𝗜𝗗𝗔 𝗞𝗔𝗥𝗡𝗘 𝗪𝗔𝗟𝗔 𝗕𝗛𝗢𝗦𝗗𝗜𝗞𝗘𝗘 𝗔𝗣𝗡𝗜 𝗠𝗔́𝗔̀ 𝗦𝗘 𝗣𝗨𝗖𝗛 𝗥Æ𝗡𝗗𝗜 𝗞𝗘 𝗕𝗔𝗖𝗛𝗘𝗘𝗘𝗘 🤩👊👤😍",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗘 𝗕𝗛𝗢𝗦𝗗𝗘 𝗠𝗘𝗜 𝗦𝗣𝗢𝗧𝗜𝗙𝗬 𝗗𝗔𝗟 𝗞𝗘 𝗟𝗢𝗙𝗜 𝗕𝗔𝗝𝗔𝗨𝗡𝗚𝗔 𝗗𝗜𝗡 𝗕𝗛𝗔𝗥 😍🎶🎶💥",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗔 𝗡𝗔𝗬𝗔 𝗥Æ𝗡𝗗𝗜 𝗞𝗛𝗔𝗡𝗔 𝗞𝗛𝗢𝗟𝗨𝗡𝗚𝗔 𝗖𝗛𝗜𝗡𝗧𝗔 𝗠𝗔𝗧 𝗞𝗔𝗥 👊🤣🤣😳",
    "𝗧𝗘𝗥𝗔 𝗕𝗔𝗔𝗣 𝗛𝗨 𝗕𝗛𝗢𝗦𝗗𝗜𝗞𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗢 𝗥Æ𝗡𝗗𝗜 𝗞𝗛𝗔𝗡𝗘 𝗣𝗘 𝗖𝗛𝗨𝗗𝗪𝗔 𝗞𝗘 𝗨𝗦 𝗣𝗔𝗜𝗦𝗘 𝗞𝗜 𝗗𝗔𝗔𝗥𝗨 𝗣𝗘𝗘𝗧𝗔 𝗛𝗨 🍷🤩🔥",
    "𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗔𝗣𝗡𝗔 𝗕𝗔𝗗𝗔 𝗦𝗔 𝗟𝗢𝗗𝗔 𝗚𝗛𝗨𝗦𝗦𝗔 𝗗𝗨𝗡𝗚𝗔𝗔 𝗞𝗔𝗟𝗟𝗔𝗔𝗣 𝗞𝗘 𝗠𝗔𝗥 𝗝𝗔𝗬𝗘𝗚𝗜 🤩😳😳🔥",
    "𝗧𝗢𝗛𝗔𝗥 𝗠𝗨𝗠𝗠𝗬 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘𝗜 𝗣𝗨𝗥𝗜 𝗞𝗜 𝗣𝗨𝗥𝗜 𝗞𝗜𝗡𝗚𝗙𝗜𝗦𝗛𝗘𝗥 𝗞𝗜 𝗕𝗢𝗧𝗧𝗟𝗘 𝗗𝗔𝗟 𝗞𝗘 𝗧𝗢𝗗 𝗗𝗨𝗡𝗚𝗔 𝗔𝗡𝗗𝗘𝗥 𝗛𝗜 😱😂🤩",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗢 𝗜𝗧𝗡𝗔 𝗖𝗛𝗢𝗗𝗨𝗡𝗚𝗔 𝗞𝗜 𝗦𝗔𝗣𝗡𝗘 𝗠𝗘𝗜 𝗕𝗛𝗜 𝗠𝗘𝗥𝗜 𝗖𝗛𝗨𝗗𝗔𝗜 𝗬𝗔𝗔𝗗 𝗞𝗔𝗥𝗘𝗚𝗜 𝗥Æ𝗡𝗗𝗜 🥳😍👊💥",
    "𝗧𝗘𝗥𝗜 𝗠𝗨𝗠𝗠𝗬 𝗔𝗨𝗥 𝗕𝗔𝗛𝗘𝗡 𝗞𝗢 𝗗𝗔𝗨𝗗𝗔 𝗗𝗔𝗨𝗗𝗔 𝗡𝗘 𝗖𝗛𝗢𝗗𝗨𝗡𝗚𝗔 𝗨𝗡𝗞𝗘 𝗡𝗢 𝗕𝗢𝗟𝗡𝗘 𝗣𝗘 𝗕𝗛𝗜 𝗟𝗔𝗡𝗗 𝗚𝗛𝗨𝗦𝗔 𝗗𝗨𝗡𝗚𝗔 𝗔𝗡𝗗𝗘𝗥 𝗧𝗔𝗞 😎😎🤣🔥",
    "𝗧𝗘𝗥𝗜 𝗠𝗨𝗠𝗠𝗬 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗞𝗢 𝗢𝗡𝗟𝗜𝗡𝗘 𝗢𝗟𝗫 𝗣𝗘 𝗕𝗘𝗖𝗛𝗨𝗡𝗚𝗔 𝗔𝗨𝗥 𝗣𝗔𝗜𝗦𝗘 𝗦𝗘 𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗔 𝗞𝗢𝗧𝗛𝗔 𝗞𝗛𝗢𝗟 𝗗𝗨𝗡𝗚𝗔 😎🤩😝😍",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗘 𝗕𝗛𝗢𝗦𝗗𝗔 𝗜𝗧𝗡𝗔 𝗖𝗛𝗢𝗗𝗨𝗡𝗚𝗔 𝗞𝗜 𝗧𝗨 𝗖𝗔𝗛 𝗞𝗘 𝗕𝗛𝗜 𝗪𝗢 𝗠𝗔𝗦𝗧 𝗖𝗛𝗨𝗗𝗔𝗜 𝗦𝗘 𝗗𝗨𝗥 𝗡𝗛𝗜 𝗝𝗔 𝗣𝗔𝗬𝗘𝗚𝗔𝗔 😏😏🤩😍",
    "𝗦𝗨𝗡 𝗕𝗘 𝗥Æ𝗡𝗗𝗜 𝗞𝗜 𝗔𝗨𝗟𝗔𝗔𝗗 𝗧𝗨 𝗔𝗣𝗡𝗜 𝗕𝗔𝗛𝗘𝗡 𝗦𝗘 𝗦𝗘𝗘𝗞𝗛 𝗞𝗨𝗖𝗛 𝗞𝗔𝗜𝗦𝗘 𝗚𝗔𝗔𝗡𝗗 𝗠𝗔𝗥𝗪𝗔𝗧𝗘 𝗛𝗔𝗜😏🤬🔥💥",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗔 𝗬𝗔𝗔𝗥 𝗛𝗨 𝗠𝗘𝗜 𝗔𝗨𝗥 𝗧𝗘𝗥𝗜 𝗕𝗔𝗛𝗘𝗡 𝗞𝗔 𝗣𝗬𝗔𝗔𝗥 𝗛𝗨 𝗠𝗘𝗜 𝗔𝗝𝗔 𝗠𝗘𝗥𝗔 𝗟𝗔𝗡𝗗 𝗖𝗛𝗢𝗢𝗦 𝗟𝗘 🤩🤣💥",
    "𝗧𝗘𝗥𝗜 𝗕𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘 𝗨𝗦𝗘𝗥𝗕𝗢𝗧 𝗟𝗔𝗚𝗔𝗔𝗨𝗡𝗚𝗔 𝗦𝗔𝗦𝗧𝗘 𝗦𝗣𝗔𝗠 𝗞𝗘 𝗖𝗛𝗢𝗗𝗘",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗚𝗔𝗔𝗡𝗗 𝗠𝗘 𝗦𝗔𝗥𝗜𝗬𝗔 𝗗𝗔𝗔𝗟 𝗗𝗨𝗡𝗚𝗔 𝗠𝗔̂𝗔̂𝗗𝗔𝗥𝗖𝗛Ø𝗗 𝗨𝗦𝗜 𝗦𝗔𝗥𝗜𝗬𝗘 𝗣𝗥 𝗧𝗔𝗡𝗚 𝗞𝗘 𝗕𝗔𝗖𝗛𝗘 𝗣𝗔𝗜𝗗𝗔 𝗛𝗢𝗡𝗚𝗘 😱😱",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘 ✋ 𝗛𝗔𝗧𝗧𝗛 𝗗𝗔𝗟𝗞𝗘 👶 𝗕𝗔𝗖𝗖𝗛𝗘 𝗡𝗜𝗞𝗔𝗟 𝗗𝗨𝗡𝗚𝗔 😍",
    "𝗧𝗘𝗥𝗜 𝗕𝗘𝗛𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘 𝗞𝗘𝗟𝗘 𝗞𝗘 𝗖𝗛𝗜𝗟𝗞𝗘 🤤🤤",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧 𝗠𝗘 𝗦𝗨𝗧𝗟𝗜 𝗕𝗢𝗠𝗕 𝗙𝗢𝗗 𝗗𝗨𝗡𝗚𝗔 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗞𝗜 𝗝𝗛𝗔𝗔𝗧𝗘 𝗝𝗔𝗟 𝗞𝗘 𝗞𝗛𝗔𝗔𝗞 𝗛𝗢 𝗝𝗔𝗬𝗘𝗚𝗜💣💋",
    "𝗧𝗘𝗥𝗜 𝗩𝗔𝗛𝗘𝗘𝗡 𝗞𝗢 𝗛𝗢𝗥𝗟𝗜𝗖𝗞𝗦 𝗣𝗘𝗘𝗟𝗔𝗞𝗘 𝗖𝗛𝗢𝗗𝗨𝗡𝗚𝗔 𝗠𝗔̂𝗔̂𝗗𝗔𝗥𝗖𝗛Ø𝗗😚",
    "𝗧𝗘𝗥𝗜 𝗜𝗧𝗘𝗠 𝗞𝗜 𝗚𝗔𝗔𝗡𝗗 𝗠𝗘 𝗟𝗨𝗡𝗗 𝗗𝗔𝗔𝗟𝗞𝗘,𝗧𝗘𝗥𝗘 𝗝𝗔𝗜𝗦𝗔 𝗘𝗞 𝗢𝗥 𝗡𝗜𝗞𝗔𝗔𝗟 𝗗𝗨𝗡𝗚𝗔 𝗠𝗔̂𝗔̂𝗗𝗔𝗥𝗖𝗛Ø𝗗😆🤤💋",
    "𝗧𝗘𝗥𝗜 𝗩𝗔𝗛𝗘𝗘𝗡 𝗞𝗢 𝗔𝗣𝗡𝗘 𝗟𝗨𝗡𝗗 𝗣𝗥 𝗜𝗧𝗡𝗔 𝗝𝗛𝗨𝗟𝗔𝗔𝗨𝗡𝗚𝗔 𝗞𝗜 𝗝𝗛𝗨𝗟𝗧𝗘 𝗝𝗛𝗨𝗟𝗧𝗘 𝗛𝗜 𝗕𝗔𝗖𝗛𝗔 𝗣𝗔𝗜𝗗𝗔 𝗞𝗥 𝗗𝗘𝗚𝗜 💦💋",
    "𝗦𝗨𝗔𝗥 𝗞𝗘 𝗣𝗜𝗟𝗟𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗢 𝗦𝗔𝗗𝗔𝗞 𝗣𝗥 𝗟𝗜𝗧𝗔𝗞𝗘 𝗖𝗛𝗢𝗗 𝗗𝗨𝗡𝗚𝗔 😂😆🤤",
    "𝗔𝗕𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗔 𝗕𝗛𝗢𝗦𝗗𝗔 𝗠𝗔𝗗𝗘𝗥𝗖𝗛𝗢𝗢𝗗 𝗞𝗥 𝗣𝗜𝗟𝗟𝗘 𝗣𝗔𝗣𝗔 𝗦𝗘 𝗟𝗔𝗗𝗘𝗚𝗔 𝗧𝗨 😼😂🤤",
    "𝗚𝗔𝗟𝗜 𝗚𝗔𝗟𝗜 𝗡𝗘 𝗦𝗛𝗢𝗥 𝗛𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀ 𝗥Æ𝗡𝗗𝗜 𝗖𝗛𝗢𝗥 𝗛𝗘 💋💋💦",
    "𝗔𝗕𝗘 𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗢 𝗖𝗛𝗢𝗗𝗨 𝗥Æ𝗡𝗗𝗜𝗞𝗘 𝗣𝗜𝗟𝗟𝗘 𝗞𝗨𝗧𝗧𝗘 𝗞𝗘 𝗖𝗛𝗢𝗗𝗘 😂👻🔥",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗢 𝗔𝗜𝗦𝗘 𝗖𝗛𝗢𝗗𝗔 𝗔𝗜𝗦𝗘 𝗖𝗛𝗢𝗗𝗔 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗔 𝗕𝗘𝗗 𝗣𝗘𝗛𝗜 𝗠𝗨𝗧𝗛 𝗗𝗜𝗔 💦💦💦💦",
    "𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗘 𝗕𝗛𝗢𝗦𝗗𝗘 𝗠𝗘 𝗔𝗔𝗔𝗚 𝗟𝗔𝗚𝗔𝗗𝗜𝗔 𝗠𝗘𝗥𝗔 𝗠𝗢𝗧𝗔 𝗟𝗨𝗡𝗗 𝗗𝗔𝗟𝗞𝗘 🔥🔥💦😆😆",
    "𝗥Æ𝗡𝗗𝗜𝗞𝗘 𝗕𝗔𝗖𝗛𝗛𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗢 𝗖𝗛𝗢𝗗𝗨 𝗖𝗛𝗔𝗟 𝗡𝗜𝗞𝗔𝗟",
    "𝗞𝗜𝗧𝗡𝗔 𝗖𝗛𝗢𝗗𝗨 𝗧𝗘𝗥𝗜 𝗥Æ𝗡𝗗𝗜 𝗠𝗔́𝗔̀𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧𝗛 𝗔𝗕𝗕 𝗔𝗣𝗡𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗢 𝗕𝗛𝗘𝗝 😆👻🤤",
    "𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗢𝗧𝗢 𝗖𝗛𝗢𝗗 𝗖𝗛𝗢𝗗𝗞𝗘 𝗣𝗨𝗥𝗔 𝗙𝗔𝗔𝗗 𝗗𝗜𝗔 𝗖𝗛𝗨𝗨́𝗧𝗛 𝗔𝗕𝗕 𝗧𝗘𝗥𝗜 𝗚𝗙 𝗞𝗢 𝗕𝗛𝗘𝗝 😆💦🤤",
    "𝗧𝗘𝗥𝗜 𝗚𝗙 𝗞𝗢 𝗘𝗧𝗡𝗔 𝗖𝗛𝗢𝗗𝗔 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗘 𝗟𝗢𝗗𝗘 𝗧𝗘𝗥𝗜 𝗚𝗙 𝗧𝗢 𝗠𝗘𝗥𝗜 𝗥Æ𝗡𝗗𝗜 𝗕𝗔𝗡𝗚𝗔𝗬𝗜 𝗔𝗕𝗕 𝗖𝗛𝗔𝗟 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗢 𝗖𝗛𝗢𝗗𝗧𝗔 𝗙𝗜𝗥𝗦𝗘 ♥️💦😆😆😆😆",
    "𝗛𝗔𝗥𝗜 𝗛𝗔𝗥𝗜 𝗚𝗛𝗔𝗔𝗦 𝗠𝗘 𝗝𝗛𝗢𝗣𝗗𝗔 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗔 𝗕𝗛𝗢𝗦𝗗𝗔 🤣🤣💋💦",
    "𝗖𝗛𝗔𝗟 𝗧𝗘𝗥𝗘 𝗕𝗔𝗔𝗣 𝗞𝗢 𝗕𝗛𝗘𝗝 𝗧𝗘𝗥𝗔 𝗕𝗔𝗦𝗞𝗔 𝗡𝗛𝗜 𝗛𝗘 𝗣𝗔𝗣𝗔 𝗦𝗘 𝗟𝗔𝗗𝗘𝗚𝗔 𝗧𝗨",
    "𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧𝗛 𝗠𝗘 𝗕𝗢𝗠𝗕 𝗗𝗔𝗟𝗞𝗘 𝗨𝗗𝗔 𝗗𝗨𝗡𝗚𝗔 𝗠𝗔́𝗔̀𝗞𝗘 𝗟𝗔𝗪𝗗𝗘",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗢 𝗧𝗥𝗔𝗜𝗡 𝗠𝗘 𝗟𝗘𝗝𝗔𝗞𝗘 𝗧𝗢𝗣 𝗕𝗘𝗗 𝗣𝗘 𝗟𝗜𝗧𝗔𝗞𝗘 𝗖𝗛𝗢𝗗 𝗗𝗨𝗡𝗚𝗔 𝗦𝗨𝗔𝗥 𝗞𝗘 𝗣𝗜𝗟𝗟𝗘 🤣🤣💋💋",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗔𝗞𝗘 𝗡𝗨𝗗𝗘𝗦 𝗚𝗢𝗢𝗚𝗟𝗘 𝗣𝗘 𝗨𝗣𝗟𝗢𝗔𝗗 𝗞𝗔𝗥𝗗𝗨𝗡𝗚𝗔 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗘 𝗟𝗔𝗘𝗪𝗗𝗘 👻🔥",
    "𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗢 𝗖𝗛𝗢𝗗 𝗖𝗛𝗢𝗗𝗞𝗘 𝗩𝗜𝗗𝗘𝗢 𝗕𝗔𝗡𝗔𝗞𝗘 𝗫𝗡𝗫𝗫.𝗖𝗢𝗠 𝗣𝗘 𝗡𝗘𝗘𝗟𝗔𝗠 𝗞𝗔𝗥𝗗𝗨𝗡𝗚𝗔 𝗞𝗨𝗧𝗧𝗘 𝗞𝗘 𝗣𝗜𝗟𝗟𝗘 💦💋",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗔𝗞𝗜 𝗖𝗛𝗨𝗗𝗔𝗜 𝗞𝗢 𝗣𝗢𝗥𝗡𝗛𝗨𝗕.𝗖𝗢𝗠 𝗣𝗘 𝗨𝗣𝗟𝗢𝗔𝗗 𝗞𝗔𝗥𝗗𝗨𝗡𝗚𝗔 𝗦𝗨𝗔𝗥 𝗞𝗘 𝗖𝗛𝗢𝗗𝗘 🤣💋💦",
    "𝗔𝗕𝗘 𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗢 𝗖𝗛𝗢𝗗𝗨 𝗥Æ𝗡𝗗𝗜𝗞𝗘 𝗕𝗔𝗖𝗛𝗛𝗘 𝗧𝗘𝗥𝗘𝗞𝗢 𝗖𝗛𝗔𝗞𝗞𝗢 𝗦𝗘 𝗣𝗜𝗟𝗪𝗔𝗩𝗨𝗡𝗚𝗔 𝗥Æ𝗡𝗗𝗜𝗞𝗘 𝗕𝗔𝗖𝗛𝗛𝗘 🤣🤣",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧𝗛 𝗙𝗔𝗔𝗗𝗞𝗘 𝗥𝗔𝗞𝗗𝗜𝗔 𝗠𝗔́𝗔̀𝗞𝗘 𝗟𝗢𝗗𝗘 𝗝𝗔𝗔 𝗔𝗕𝗕 𝗦𝗜𝗟𝗪𝗔𝗟𝗘 👄👄",
    "𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧𝗛 𝗠𝗘 𝗠𝗘𝗥𝗔 𝗟𝗨𝗡𝗗 𝗞𝗔𝗔𝗟𝗔",
    "𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗟𝗘𝗧𝗜 𝗠𝗘𝗥𝗜 𝗟𝗨𝗡𝗗 𝗕𝗔𝗗𝗘 𝗠𝗔𝗦𝗧𝗜 𝗦𝗘 𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗢 𝗠𝗘𝗡𝗘 𝗖𝗛𝗢𝗗 𝗗𝗔𝗟𝗔 𝗕𝗢𝗛𝗢𝗧 𝗦𝗔𝗦𝗧𝗘 𝗦𝗘",
    "𝗕𝗘𝗧𝗘 𝗧𝗨 𝗕𝗔𝗔𝗣 𝗦𝗘 𝗟𝗘𝗚𝗔 𝗣𝗔𝗡𝗚𝗔 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗔 𝗞𝗢 𝗖𝗛𝗢𝗗 𝗗𝗨𝗡𝗚𝗔 𝗞𝗔𝗥𝗞𝗘 𝗡𝗔𝗡𝗚𝗔 💦💋",
    "𝗛𝗔𝗛𝗔𝗛𝗔𝗛 𝗠𝗘𝗥𝗘 𝗕𝗘𝗧𝗘 𝗔𝗚𝗟𝗜 𝗕𝗔𝗔𝗥 𝗔𝗣𝗡𝗜 𝗠𝗔́𝗔̀𝗞𝗢 𝗟𝗘𝗞𝗘 𝗔𝗔𝗬𝗔 𝗠𝗔𝗧𝗛 𝗞𝗔𝗧 𝗢𝗥 𝗠𝗘𝗥𝗘 𝗠𝗢𝗧𝗘 𝗟𝗨𝗡𝗗 𝗦𝗘 𝗖𝗛𝗨𝗗𝗪𝗔𝗬𝗔 𝗠𝗔𝗧𝗛 𝗞𝗔𝗥",
    "𝗖𝗛𝗔𝗟 𝗕𝗘𝗧𝗔 𝗧𝗨𝗝𝗛𝗘 𝗠𝗔́𝗔̀𝗙 𝗞𝗜𝗔 🤣 𝗔𝗕𝗕 𝗔𝗣𝗡𝗜 𝗚𝗙 𝗞𝗢 𝗕𝗛𝗘𝗝",
    "𝗦𝗛𝗔𝗥𝗔𝗠 𝗞𝗔𝗥 𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗔 𝗕𝗛𝗢𝗦𝗗𝗔 𝗞𝗜𝗧𝗡𝗔 𝗚𝗔𝗔𝗟𝗜𝗔 𝗦𝗨𝗡𝗪𝗔𝗬𝗘𝗚𝗔 𝗔𝗣𝗡𝗜 𝗠𝗔́𝗔̀𝗔 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗘 𝗨𝗣𝗘𝗥",
    "𝗔𝗕𝗘 𝗥Æ𝗡𝗗𝗜𝗞𝗘 𝗕𝗔𝗖𝗛𝗛𝗘 𝗔𝗨𝗞𝗔𝗧 𝗡𝗛𝗜 𝗛𝗘𝗧𝗢 𝗔𝗣𝗡𝗜 𝗥Æ𝗡𝗗𝗜 𝗠𝗔́𝗔̀𝗞𝗢 𝗟𝗘𝗞𝗘 𝗔𝗔𝗬𝗔 𝗠𝗔𝗧𝗛 𝗞𝗔𝗥 𝗛𝗔𝗛𝗔𝗛𝗔𝗛𝗔",
    "𝗞𝗜𝗗𝗭 𝗠𝗔̂𝗔̂𝗗𝗔𝗥𝗖𝗛Ø𝗗 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗢 𝗖𝗛𝗢𝗗 𝗖𝗛𝗢𝗗𝗞𝗘 𝗧𝗘𝗥𝗥 𝗟𝗜𝗬𝗘 𝗕𝗛𝗔𝗜 𝗗𝗘𝗗𝗜𝗬𝗔",
    "𝗝𝗨𝗡𝗚𝗟𝗘 𝗠𝗘 𝗡𝗔𝗖𝗛𝗧𝗔 𝗛𝗘 𝗠𝗢𝗥𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗜 𝗖𝗛𝗨𝗗𝗔𝗜 𝗗𝗘𝗞𝗞𝗘 𝗦𝗔𝗕 𝗕𝗢𝗟𝗧𝗘 𝗢𝗡𝗖𝗘 𝗠𝗢𝗥𝗘 𝗢𝗡𝗖𝗘 𝗠𝗢𝗥𝗘 🤣🤣💦💋",
    "𝗚𝗔𝗟𝗜 𝗚𝗔𝗟𝗜 𝗠𝗘 𝗥𝗘𝗛𝗧𝗔 𝗛𝗘 𝗦𝗔𝗡𝗗 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗢 𝗖𝗛𝗢𝗗 𝗗𝗔𝗟𝗔 𝗢𝗥 𝗕𝗔𝗡𝗔 𝗗𝗜𝗔 𝗥𝗔𝗡𝗗 🤤🤣",
    "𝗦𝗔𝗕 𝗕𝗢𝗟𝗧𝗘 𝗠𝗨𝗝𝗛𝗞𝗢 𝗣𝗔𝗣𝗔 𝗞𝗬𝗢𝗨𝗡𝗞𝗜 𝗠𝗘𝗡𝗘 𝗕𝗔𝗡𝗔𝗗𝗜𝗔 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗢 𝗣𝗥𝗘𝗚𝗡𝗘𝗡𝗧 🤣🤣",
    "𝗦𝗨𝗔𝗥 𝗞𝗘 𝗣𝗜𝗟𝗟𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧𝗛 𝗠𝗘 𝗦𝗨𝗔𝗥 𝗞𝗔 𝗟𝗢𝗨𝗗𝗔 𝗢𝗥 𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧𝗛 𝗠𝗘 𝗠𝗘𝗥𝗔 𝗟𝗢𝗗𝗔",
    "𝗖𝗛𝗔𝗟 𝗖𝗛𝗔𝗟 𝗔𝗣𝗡𝗜 𝗠𝗔́𝗔̀𝗞𝗜 𝗖𝗛𝗨𝗖𝗛𝗜𝗬𝗔 𝗗𝗜𝗞𝗔",
    "𝗛𝗔𝗛𝗔𝗛𝗔𝗛𝗔 𝗕𝗔𝗖𝗛𝗛𝗘 𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗔𝗞𝗢 𝗖𝗛𝗢𝗗 𝗗𝗜𝗔 𝗡𝗔𝗡𝗚𝗔 𝗞𝗔𝗥𝗞𝗘",
    "𝗧𝗘𝗥𝗜 𝗚𝗙 𝗛𝗘 𝗕𝗔𝗗𝗜 𝗦𝗘𝗫𝗬 𝗨𝗦𝗞𝗢 𝗣𝗜𝗟𝗔𝗞𝗘 𝗖𝗛𝗢𝗢𝗗𝗘𝗡𝗚𝗘 𝗣𝗘𝗣𝗦𝗜",
    "2 𝗥𝗨𝗣𝗔𝗬 𝗞𝗜 𝗣𝗘𝗣𝗦𝗜 𝗧𝗘𝗥𝗜 𝗠𝗨𝗠𝗠𝗬 𝗦𝗔𝗕𝗦𝗘 𝗦𝗘𝗫𝗬 💋💦",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗢 𝗖𝗛𝗘𝗘𝗠𝗦 𝗦𝗘 𝗖𝗛𝗨𝗗𝗪𝗔𝗩𝗨𝗡𝗚𝗔 𝗠𝗔𝗗𝗘𝗥𝗖𝗛𝗢𝗢𝗗 𝗞𝗘 𝗣𝗜𝗟𝗟𝗘 💦🤣",
    "𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗜 𝗖𝗛𝗨𝗨́𝗧𝗛 𝗠𝗘 𝗠𝗨𝗧𝗛𝗞𝗘 𝗙𝗔𝗥𝗔𝗥 𝗛𝗢𝗝𝗔𝗩𝗨𝗡𝗚𝗔 𝗛𝗨𝗜 𝗛𝗨𝗜 𝗛𝗨𝗜",
    "𝗦𝗣𝗘𝗘𝗗 𝗟𝗔𝗔𝗔 𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗖𝗛𝗢𝗗𝗨 𝗥Æ𝗡𝗗𝗜𝗞𝗘 𝗣𝗜𝗟𝗟𝗘 💋💦🤣",
    "𝗔𝗥𝗘 𝗥𝗘 𝗠𝗘𝗥𝗘 𝗕𝗘𝗧𝗘 𝗞𝗬𝗢𝗨𝗡 𝗦𝗣𝗘𝗘𝗗 𝗣𝗔𝗞𝗔𝗗 𝗡𝗔 𝗣𝗔𝗔𝗔 𝗥𝗔𝗛𝗔 𝗔𝗣𝗡𝗘 𝗕𝗔𝗔𝗣 𝗞𝗔 𝗛𝗔𝗛𝗔𝗛🤣🤣",
    "𝗦𝗨𝗡 𝗦𝗨𝗡 𝗦𝗨𝗔𝗥 𝗞𝗘 𝗣𝗜𝗟𝗟𝗘 𝗝𝗛𝗔𝗡𝗧𝗢 𝗞𝗘 𝗦𝗢𝗨𝗗𝗔𝗚𝗔𝗥 𝗔𝗣𝗡𝗜 𝗠𝗨𝗠𝗠𝗬 𝗞𝗜 𝗡𝗨𝗗𝗘𝗦 𝗕𝗛𝗘𝗝",
    "𝗔𝗕𝗘 𝗦𝗨𝗡 𝗟𝗢𝗗𝗘 𝗧𝗘𝗥𝗜 𝗕𝗘́𝗛𝗘𝗡 𝗞𝗔 𝗕𝗛𝗢𝗦𝗗𝗔 𝗙𝗔𝗔𝗗 𝗗𝗨𝗡𝗚𝗔",
    "𝗧𝗘𝗥𝗜 𝗠𝗔́𝗔̀𝗞𝗢 𝗞𝗛𝗨𝗟𝗘 𝗕𝗔𝗝𝗔𝗥 𝗠𝗘 𝗖𝗛𝗢𝗗 𝗗𝗔𝗟𝗔 🤣🤣💋",
    "𝗦𝗛𝗔𝗥𝗔𝗠 𝗔𝗔 𝗚𝗬𝗜 𝗛𝗔𝗜 𝗧𝗢 𝗡𝗔𝗭𝗥𝗘𝗡 𝗝𝗛𝗨𝗞𝗔 𝗟𝗜𝗝𝗜𝗬𝗘 𝗢𝗥 𝗔𝗚𝗔𝗥 𝗟𝗨𝗡𝗗 𝗠𝗘 𝗗𝗔𝗠 𝗡𝗛𝗜 𝗧𝗢 𝗦𝗛𝗜𝗟𝗔𝗝𝗘𝗘𝗧 𝗞𝗛𝗔 𝗟𝗜𝗝𝗜𝗬𝗘...🤣😂😂"
]

REPLYRAID_MESSAGES = [
    "MADARCHOD",
    "BHOSDIKE",
    "LAAAWEEE KE BAAAAAL",
    "MAAAAR KI JHAAAAT KE BBBBBAAAAALLLLL",
    "MADRCHOD..",
    "TERI MA KI CHUT..",
    "LWDE KE BAAALLL.",
    "MACHAR KI JHAAT KE BAAALLLL",
    "TERI MA KI CHUT M DU TAPA TAP?",
    "TERI MA KA BHOSDAA",
    "TERI BHN SBSBE BDI RANDI.",
    "TERI MA OSSE BADI RANDDDDD",
    "TERA BAAP CHKAAAA",
    "KITNI CHODU TERI MA AB OR..",
    "TERI MA CHOD DI HM NE",
    "MIGHTY !!  BAAP BOLTE",
    "TERI MA KE STH REELS BNEGA ROAD PEE",
    "TERI MA KI CHUT EK DAM TOP SEXY",
    "MALUM NA PHR KESE LETA HU M TERI MA KI CHUT TAPA TAPPPPP",
    "LUND KE CHODE TU KEREGA TYPIN",
    "SPEED PKD LWDEEEE",
    "BAAP KI SPEED MTCH KRRR",
    "LWDEEE",
    "PAPA KI SPEED MTCH NHI HO RHI KYA",
    "ALE ALE MELA BCHAAAA",
    "[Bʟᴀᴄᴋᴏᴜᴛ](t.me/PYTH0NXD) TERA BAAP !!",
    "CHUD GYA PAPA SEEE",
    "KISAN KO KHODNA OR",
    "SALE RAPEKL KRDKA TERA",
    "HAHAHAAAAA",
    "KIDSSSS",
    "BACHHE TERI MAA KI CHUTT",
    "TERI BHEN KI CHUTT BHOSDIWALE",
    "TERI MA CHUD GYI AB FRAR MT HONA",
    "YE LDNGE BAPP SE",
    "KIDSSS FRAR HAHAHH",
    "BHEN KE LWDE SHRM KR",
    "KITNI GLIYA PDWEGA APNI MA KO",
    "NALLEE",
    "SUAR KE PILLE TERI MAAKO SADAK PR LITAKE CHOD DUNGA 😂😆🤤",
    "ABE TERI MAAKA BHOSDA MADERCHOOD KR PILLE PAPA SE LADEGA TU 😼😂🤤",
    "GALI GALI NE SHOR HE TERI MAA RANDI CHOR HE 💋💋💦",
    "ABE TERI BEHEN KO CHODU RANDIKE PILLE KUTTE KE CHODE 😂👻🔥",
    "TERI MAAKO AISE CHODA AISE CHODA TERI MAAA BED PEHI MUTH DIA 💦💦💦💦",
    "TERI BEHEN KE BHOSDE ME AAAG LAGADIA MERA MOTA LUND DALKE 🔥🔥💦😆😆",
    "RANDIKE BACHHE TERI MAAKO CHODU CHAL NIKAL",
    "KITNA CHODU TERI RANDI MAAKI CHUTH ABB APNI BEHEN KO BHEJ 😆👻🤤",
    "TERI BEHEN KOTO CHOD CHODKE PURA FAAD DIA CHUTH ABB TERI GF KO BHEJ 😆💦🤤",
    "TERI GF KO ETNA CHODA BEHEN KE LODE TERI GF TO MERI RANDI BANGAYI ABB CHAL TERI MAAKO CHODTA FIRSE ♥️💦😆😆😆😆",
    "HARI HARI GHAAS ME JHOPDA TERI MAAKA BHOSDA 🤣🤣💋💦",
    "CHAL TERE BAAP KO BHEJ TERA BASKA NHI HE PAPA SE LADEGA TU",
    "TERI BEHEN KI CHUTH ME BOMB DALKE UDA DUNGA MAAKE LAWDE",
    "TERI MAAKO TRAIN ME LEJAKE TOP BED PE LITAKE CHOD DUNGA SUAR KE PILLE 🤣🤣💋💋",
    "TERI MAAAKE NUDES GOOGLE PE UPLOAD KARDUNGA BEHEN KE LAEWDE 👻🔥",
    "TERI MAAAKE NUDES GOOGLE PE UPLOAD KARDUNGA BEHEN KE LAEWDE 👻🔥",
    "TERI BEHEN KO CHOD CHODKE VIDEO BANAKE XNXX.COM PE NEELAM KARDUNGA KUTTE KE PILLE 💦💋",
    "TERI MAAAKI CHUDAI KO PORNHUB.COM PE UPLOAD KARDUNGA SUAR KE CHODE 🤣💋💦",
    "ABE TERI BEHEN KO CHODU RANDIKE BACHHE TEREKO CHAKKO SE PILWAVUNGA RANDIKE BACHHE 🤣🤣",
    "TERI MAAKI CHUTH FAADKE RAKDIA MAAKE LODE JAA ABB SILWALE 👄👄",
    "TERI BEHEN KI CHUTH ME MERA LUND KAALA",
    "TERI BEHEN LETI MERI LUND BADE MASTI SE TERI BEHEN KO MENE CHOD DALA BOHOT SASTE SE",
    "BETE TU BAAP SE LEGA PANGA TERI MAAA KO CHOD DUNGA KARKE NANGA 💦💋",
    "HAHAHAH MERE BETE AGLI BAAR APNI MAAKO LEKE AAYA MATH KAT OR MERE MOTE LUND SE CHUDWAYA MATH KAR",
    "CHAL BETA TUJHE MAAF KIA 🤣 ABB APNI GF KO BHEJ",
    "SHARAM KAR TERI BEHEN KA BHOSDA KITNA GAALIA SUNWAYEGA APNI MAAA BEHEN KE UPER",
    "ABE RANDIKE BACHHE AUKAT NHI HETO APNI RANDI MAAKO LEKE AAYA MATH KAR HAHAHAHA",
    "KIDZ MADARCHOD TERI MAAKO CHOD CHODKE TERR LIYE BHAI DEDIYA",
    "JUNGLE ME NACHTA HE MORE TERI MAAKI CHUDAI DEKKE SAB BOLTE ONCE MORE ONCE MORE 🤣🤣💦💋",
    "GALI GALI ME REHTA HE SAND TERI MAAKO CHOD DALA OR BANA DIA RAND 🤤🤣",
    "SAB BOLTE MUJHKO PAPA KYOUNKI MENE BANADIA TERI MAAKO PREGNENT 🤣🤣",
    "SUAR KE PILLE TERI MAAKI CHUTH ME SUAR KA LOUDA OR TERI BEHEN KI CHUTH ME MERA LODA",
    "CHAL CHAL APNI MAAKI CHUCHIYA DIKA",
    "HAHAHAHA BACHHE TERI MAAAKO CHOD DIA NANGA KARKE",
    "TERI GF HE BADI SEXY USKO PILAKE CHOODENGE PEPSI",
    "2 RUPAY KI PEPSI TERI MUMMY SABSE SEXY 💋💦",
    "TERI MAAKO CHEEMS SE CHUDWAVUNGA MADERCHOOD KE PILLE 💦🤣",
    "TERI BEHEN KI CHUTH ME MUTHKE FARAR HOJAVUNGA HUI HUI HUI",
    "SPEED LAAA TERI BEHEN CHODU RANDIKE PILLE 💋💦🤣",
    "ARE RE MERE BETE KYOUN SPEED PAKAD NA PAAA RAHA APNE BAAP KA HAHAH🤣🤣",
    "SUN SUN SUAR KE PILLE JHANTO KE SOUDAGAR APNI MUMMY KI NUDES BHEJ",
    "ABE SUN LODE TERI BEHEN KA BHOSDA FAAD DUNGA",
    "TERI MAAKO KHULE BAJAR ME CHOD DALA 🤣🤣💋",
    "SHRM KR",
    "MERE LUND KE BAAAAALLLLL",
    "KITNI GLIYA PDWYGA APNI MA BHEN KO",
    "RNDI KE LDKEEEEEEEEE",
    "KIDSSSSSSSSSSSS",
    "Apni gaand mein muthi daal",
    "Apni lund choos",
    "Apni ma ko ja choos",
    "Bhen ke laude",
    "Bhen ke takke",
    "Abla TERA KHAN DAN CHODNE KI BARIII",
    "BETE TERI MA SBSE BDI RAND",
    "LUND KE BAAAL JHAT KE PISSSUUUUUUU",
    "LUND PE LTKIT MAAALLLL KI BOND H TUUU",
    "KASH OS DIN MUTH MRKE SOJTA M TUN PAIDA NA HOTAA",
    "GLTI KRDI TUJW PAIDA KRKE",
    "SPEED PKDDD",
    "Gaand main LWDA DAL LE APNI MERAAA",
    "Gaand mein bambu DEDUNGAAAAAA",
    "GAND FTI KE BALKKK",
    "Gote kitne bhi bade ho, lund ke niche hi rehte hai",
    "Hazaar lund teri gaand main",
    "Jhaant ke pissu-",
    "TERI MA KI KALI CHUT",
    "Khotey ki aulad",
    "Kutte ka awlad",
    "Kutte ki jat",
    "Kutte ke tatte",
    "TETI MA KI.CHUT , tERI MA RNDIIIIIIIIIIIIIIIIIIII",
    "Lavde ke bal",
    "muh mei lele",
    "Lund Ke Pasine",
    "MERE LWDE KE BAAAAALLL",
    "HAHAHAAAAAA",
    "CHUD GYAAAAA",
    "Randi khanE KI ULADDD",
    "Sadi hui gaand",
    "Teri gaand main kute ka lund",
    "Teri maa ka bhosda",
    "Teri maa ki chut",
    "Tere gaand mein keede paday",
    "Ullu ke pathe",
    "SUNN MADERCHOD",
    "TERI MAA KA BHOSDA",
    "BEHEN K LUND",
    "TERI MAA KA CHUT KI CHTNIIII",
    "MERA LAWDA LELE TU AGAR CHAIYE TOH",
    "GAANDU",
    "CHUTIYA",
    "TERI MAA KI CHUT PE JCB CHADHAA DUNGA",
    "SAMJHAA LAWDE",
    "YA DU TERE GAAND ME TAPAA TAP��",
    "TERI BEHEN MERA ROZ LETI HAI",
    "TERI GF K SAATH MMS BANAA CHUKA HU���不�不",
    "TU CHUTIYA TERA KHANDAAN CHUTIYA",
    "AUR KITNA BOLU BEY MANN BHAR GAYA MERA�不",
    "TERIIIIII MAAAA KI CHUTTT ME ABCD LIKH DUNGA MAA KE LODE",
    "TERI MAA KO LEKAR MAI FARAR",
    "RANIDIII",
    "BACHEE",
    "CHODU",
    "RANDI",
    "RANDI KE PILLE",
    "TERIIIII MAAA KO BHEJJJ",
    "TERAA BAAAAP HU",
    "teri MAA KI CHUT ME HAAT DAALLKE BHAAG JAANUGA",
    "Teri maa KO SARAK PE LETAA DUNGA",
    "TERI MAA KO GB ROAD PE LEJAKE BECH DUNGA",
    "Teri maa KI CHUT MÉ KAALI MITCH",
    "TERI MAA SASTI RANDI HAI",
    "TERI MAA KI CHUT ME KABUTAR DAAL KE SOUP BANAUNGA MADARCHOD",
    "TERI MAAA RANDI HAI",
    "TERI MAAA KI CHUT ME DETOL DAAL DUNGA MADARCHOD",
    "TERI MAA KAAA BHOSDAA",
    "TERI MAA KI CHUT ME LAPTOP",
    "Teri maa RANDI HAI",
    "TERI MAA KO BISTAR PE LETAAKE CHODUNGA",
    "TERI MAA KO AMERICA GHUMAAUNGA MADARCHOD",
    "TERI MAA KI CHUT ME NAARIYAL PHOR DUNGA",
    "TERI MAA KE GAND ME DETOL DAAL DUNGA",
    "TERI MAAA KO HORLICKS PILAUNGA MADARCHOD",
    "TERI MAA KO SARAK PE LETAAA DUNGAAA",
    "TERI MAA KAA BHOSDA",
    "MERAAA LUND PAKAD LE MADARCHOD",
    "CHUP TERI MAA AKAA BHOSDAA",
    "TERIII MAA CHUF GEYII KYAAA LAWDEEE",
    "TERIII MAA KAA BJSODAAA",
    "MADARXHODDD",
    "TERIUUI MAAA KAA BHSODAAA",
    "TERIIIIII BEHENNNN KO CHODDDUUUU MADARXHODDDD",
    "NIKAL MADARCHOD",
    "RANDI KE BACHE",
    "TERA MAA MERI FAN",
    "TERI SEXY BAHEN KI CHUT OP"
]

GROUP = [-1001603822916]


PSPAM_MESSAGES= [
        "https://te.legra.ph/file/a66008b78909b431fc92b.mp4",
        "https://te.legra.ph/file/0ab82f535e1193d09c0e4.mp4",
        "https://te.legra.ph/file/1ab9cde9388117db9d26c.mp4",
        "https://te.legra.ph/file/75e49339469dbf9ad1dd2.mp4",
        "https://telegra.ph/file/9bcc076fd81dfe3feb291.mp4",
        "https://telegra.ph/file/b7a1a42429a65f64e67af.mp4",
        "https://telegra.ph/file/dc3da5a3eb77ae20fa21d.mp4",
        "https://telegra.ph/file/7b15fbca08ae1e73e559c.mp4",
        "https://telegra.ph/file/a9c1dea3f34925bb60686.mp4",
        "https://telegra.ph/file/913b4e567b7f435b7f0db.mp4",
        "https://telegra.ph/file/5a5d1a919a97af2314955.mp4",
        "https://telegra.ph/file/0f8b903669600d304cbe4.mp4",
        "https://telegra.ph/file/f3816b54c9eb7617356b6.mp4",
        "https://telegra.ph/file/516dbaa03fde1aaa70633.mp4",
        "https://telegra.ph/file/07bba6ead0f1e381b1bd1.mp4",
        "https://telegra.ph/file/0a4f7935df9b4ab8d62ed.mp4",
        "https://telegra.ph/file/40966bf68c0e4dbe18058.mp4",
        "https://telegra.ph/file/50637aa9c04d136687523.mp4",
        "https://telegra.ph/file/b81c0b0e491da73e64260.mp4",
        "https://telegra.ph/file/4ddf5f29783d92ae03804.mp4",
        "https://telegra.ph/file/4037dc2517b702cc208b1.mp4",
        "https://telegra.ph/file/33cebe2798c15d52a2547.mp4",
        "https://telegra.ph/file/4dc3c8b03616da516104a.mp4",
        "https://telegra.ph/file/6b148dace4d987fae8f3e.mp4",
        "https://telegra.ph/file/8cb081db4eeed88767635.mp4",
        "https://telegra.ph/file/98d3eb94e6f00ed56ef91.mp4",
        "https://telegra.ph/file/1fb387cf99e057b62d75d.mp4",
        "https://telegra.ph/file/6e1161f63879c07a1f213.mp4",
        "https://telegra.ph/file/0bf4defb9540d2fa6d277.mp4",
        "https://telegra.ph/file/d5f8280754d9aa5dffa6a.mp4",
        "https://telegra.ph/file/0f23807ed1930704e2bef.jpg",
        "https://telegra.ph/file/c49280b8f1dcecaf86c00.jpg",
        "https://telegra.ph/file/f483400ff141de73767ca.jpg",
        "https://telegra.ph/file/1543bbea4e3c1abb6764a.jpg",
        "https://telegra.ph/file/a0d77be0d769c7cd334ab.jpg",
        "https://telegra.ph/file/6c6e93860527d2f577df8.jpg",
        "https://telegra.ph/file/d987b0e72eb3bb4801f01.jpg",
        "https://telegra.ph/file/b434999287d3580250960.jpg",
        "https://telegra.ph/file/0729cc082bf97347988f7.jpg",
        "https://telegra.ph/file/bb96d25df82178a2892e7.jpg",
        "https://telegra.ph/file/be73515791ea33be92a7d.jpg",
        "https://telegra.ph/file/fe234d6273093282d2dcc.jpg",
        "https://telegra.ph/file/66254bb72aa8094d38250.jpg",
        "https://telegra.ph/file/44bdaf37e5f7bdfc53ac6.jpg",
        "https://telegra.ph/file/e561ee1e1ca88db7e8038.jpg",
        "https://telegra.ph/file/f1960ccfc866b29ea5ad2.jpg",
        "https://telegra.ph/file/97622cad291472fb3c4aa.jpg",
        "https://telegra.ph/file/a46e316b413e9dc43e91b.jpg",
        "https://telegra.ph/file/497580fc3bddc21e0e162.jpg",
        "https://telegra.ph/file/3e86cc6cab06a6e2bde82.jpg",
        "https://telegra.ph/file/83140e2c57ddd95f310e6.jpg",
        "https://telegra.ph/file/2b20f8509d9437e94fed5.jpg",
        "https://telegra.ph/file/571960dcee4fce56698a4.jpg",
        "https://telegra.ph/file/25929a0b49452d8946c14.mp4",
        "https://telegra.ph/file/f5c9ceded3ee6e76a5931.jpg",
        "https://telegra.ph/file/a8bf6c6df8a48e4a306ca.jpg",
        "https://telegra.ph/file/af9e3f98da0bd937adf6e.jpg",
        "https://telegra.ph/file/2fcccbc72c57b6892d23a.jpg",
        "https://telegra.ph/file/843109296a90b8a6c5f68.jpg"
]


MRAID_MESSAGES = [
    "Tere naalo challiye haseen koyi NA 😁😁",
    "Taare chann ambar zameen koyi nA",
    "Main Jado Tere Mode Utte Sir Rakheya🧐🧐",
    "Eh Ton Sachi Sama Vi Haseen Koi Na😖😖",
    "Sohniyan Vi Laggan Giyan Fer Walian😍😍",
    "Galan Nal Jado Takraiyan Waliyan🥰🥰",
    "Tare Dekhi Labh Labh Kiven Harde😁😁",
    "Tu Bala Ch Lakoiyan Jado Ratan Kaliyan😒😒",
    "Main Sab Kuj Har Tere Utton De’unga😌😌",
    "Sab Kuj War Tere Utton De’unga😉😉",
    "Akhir Ch Jan Tainu De’un Apni😎😎",
    "Chala Tainu Bhavein Pehli War De’unga😚😚",
    "Han Main Cheti Cheti Lawan😫😫",
    "Tere Nal Laini an😣😣",
    "Samay Da Tan Bhora Vi Yakeen Koi Na🥺🥺",
    "Tere Nalo Jhaliye Haseen Koi Na🥰🥰",
    "Tare Chann Ambar Zameen Koi Na😘😘",
    "Tu Yar Mera Tu Hi Ae Sahara AdiyE",
    "Main Pani Tera Mera Tu Kinara Adiye",
    "Phul Ban Jai Main Khushboo Bann Ju",
    "Deevan Bani Mera Teri Lau Ban Ju",
    "Haye Ujadiyan Thawan Te Banate Bag Ne",
    "Teriyan Ankhan Ne Kitte Jadu Yad Ne",
    "Jado Wang Kolon Phadi Vi Ni KassKe",
    "Totte Sambh Rakhe Tutte Hoye Kach De",
    "Han Ki Dil Yadan Rakhda Ae, Sambh Sambh Ke",
    "Hor Dil Sajjna Machine Koi Na",
    "Tere Nalo Jhaliye Haseen Koi Na",
    "Tare Chann Ambar Zameen Koi Na",
    "Main Jado Tere Mode Utte Sir Rakheya",
    "Eh Ton Sachi Sama Vi Haseen Koi Na",
    "Kine Din Hogye Meri Akh Soi Na",
    "Tere Ton Bagair Mera Aithe Koi Na",
    "Tu Bhukh Vi Ae Tu Hi Ae Guzara Adiye",
    "Mannu Sab Kari Tu Ishara Adiye",
    "Ho Khaure Kinni War Seene Vich Khubiyan",
    "Surme De Vich Dovein Ankhan Dubbiyan",
    "Kini Sohni Lagge Jadon Chup Kar Je",
    "Jandi Jandi Shaman Nu Vi Dhup Kar Je",
    "Haye Main Paun Farmaishi Rang Tere Sohniye",
    "Unj Bahotan Gifty Shaukeen Koi Na",
    "Tare Chann Ambar Zameen Koi Na🥰🥰",
    "Tere Nalo Jhaliye Haseen Koi Na😍😍",
    "Main Jado Tere Mode Utte Sir Rakheya😁😁",
    "Eh Ton Sachi Sama Vi Haseen Koi Na😒😒",
    "Kanna Wich Jhumka👀👀",
    "Akhan Wich Surma🙈🙈",
    "Ho Jaise Strawberry Candy😋😋",
    "Nakk Utte Koka🤨🤨",
    "Jeena Kare Aukha🤭🤭",
    "Haye Meri Jaan Kadd Laindi😌😌",
    "Tere Nakhre Haye Tauba Sanu Maarde🤫🤫",
    "Ho Gaya Hai Mera Baby Bura HaaL😊😊",
    "Sachi Lut Gaye Hum Tere Is Pyar Mein😏😏",
    "Jeeni Zindagi Hai Bas Tere Naal😚😚",
    "I Love YoU SO MUCH 😍😍",
    "cause I Love You 😘😘",
    "Sapno Mein Mere AayI😝😝",
    "Baby! Lage Sohna Kitna PyarA😚😚",
    "Sapno Mein Mere Aayi😝😝",
    "Uff Oh Phir Neendein Hi Churayi😜😜",
    "Oh No! Tera Husan Nazara🥰🥰",
    "Tainu Diamond Mundri Pehnawa😎😎",
    "Naale Duniya Sari Ghumawa🙈🙈",
    "Chhoti-Chhoti Gallan Utte Main Hasavaan💙💙",
    "Yaara Kade Vi Na Tainu Main Rulawaan🙊🙊",
    "cause I Love You  🙈🙈",
    "I Love You ❤️❤️",
    "cause I Love You🙈🙈",
    "Yaari Laawan Sachi YaarI💫💫",
    "Tu Jaan Ton Vi Pyari😁😁",
    "Will Love You To The Moon And Back😆😆",
    "Hogi Saza Na Koyi Hogi😙😙",
    "Chahe Karun Chori Chaand Taare😉😉",
    "Imma Give You Them😅😅",
    "Yaari Laavan Sachi YaarI😘😘",
    "Tu Jaan Ton Vi PyarI😆😆",
    "Will Love You To The Moon And Back💕💕",
    "Hogee Sazaa Na Koyi Hogi💓💓",
    "Chahe Karun Chori Chaand Taare🥺🥺",
    "Imma Give You Them🥵🥵",
    "Puri Karunga Main Teri Sari Khahishein😁😁",
    "Tera Rakhanga Main Rajj Ke Khayal😘😘",
    "Kitni Khoobiyan Hai Tere Is Yaar Mein🥰🥰",
    "Aaja Bahon Mein Tu Bahein Bas Daal😂😂",
    "Aur Hota Nahi Ab Intezar🤩🤩",
    "Aur Hota Nahee Ab Intezaar😘😘",
    "cause I Love You 😍😍",
    "I Love YoU 😙😙",
    "cause I Love You",
    "I Love YoU SOOOOOOOOOOOOOOOOOO MUCHHHHHHHHHHHHHHHHHHHHH 😘😘",
    "WILL U BE MINE FOREVER??🤔🤔",
    "Je tu akh te main aan kaajal ve😌😌",
    "Tu baarish te main baadal ve🤫🤫",
    "Tu deewana main aan paagal ve🤪🤪",
    "Sohneya sohneya☺️☺️",
    "Je tu chann te main aan taara ve🤗🤗",
    "Main lehar te tu kinara ve😶😶",
    "Main aadha te tu saara ve🤗🤗",
    "Sohneya sohneya😗😗",
    "Tu jahan hai main wahan😘😘",
    "Tere bin main hoon hi kya🥲🥲",
    "Tere bin chehre se mere🤔🤔",
    "Udd jaaye rang ve😅😅",
    "Tujhko paane ke liye huM😁😁",
    "Roz mangein mannat ve🙈🙈",
    "Duniya to kya cheez hai yaara🙉🙉",
    "Tujhko paane ke liye hum😌😌",
    "Roz mangein mannat ve🤫🤫",
    "Duniya to kya cheez hai yaara🤔🤔",
    "Na parwah mainu apni aa😁😁",
    "Na parwah mainu duniya di👅👅",
    "Na parwah mainu apni aa😅😅",
    "Tere ton juda nahi kar sakdi🤬🤬",
    "Koyi taakat mainu duniya di😈😈",
    "Dooron aa jaave teri khushbu😎😎",
    "Akhan hun band taan vi vekh lawan😍😍",
    "Teri gali vich mera auna har roz😋😋",
    "Tera ghar jadon aave matha tek lawan😌😌",
    "Nirmaan tujhko dekh ke😏😏",
    "Aa jaave himmat ve😉😉",
    "Tujhko paane ke liye hum😊😊",
    "Roz mangein mannat ve😉😉",
    "Duniya to kya cheez hai yaara😌😌",
    "Thukra denge jannat ve😍😍",
    "Tujhko paane ke liye hum🤫🤫",
    "Roz mangein mannat ve😁😁",
    "Duniya to kya cheez hai yaara😏😏",
    "Thukra denge jannat ve😌😌",
    "SO MISS 😶😶",
    "KYA SOCHA APNE BAARE MAIN😆😆",
    "BADI MUSHKIL SE YEH SAB KARA H RE🥵🥵",
    "PAHLE PURA BOT HI KANG MAAR DIYA BUT🤫🤫",
    "WAHI ERROR AAYE JO AATE THE🥲🥲",
    "BUT TUMHARA HO CHUKA WALA BF😎😎",
    "AND FUTURE HUSBAND JO BANNE WALA THA WO BHOT SMART H RE😌😌",
    "ISS BAAR BOT BANAYA AND CHOTA SA EDIT KARA BAS😁😁",
    "AUR DEKO ABHI TUM USSI BOT SE YEH PADH PAA RHI😂😂",
    "HEHE BTW YEH CHORO MEKO NA TUMSE😶😶",
    "KUCH PUCHNA THA KI ME🤔🤔",
    "TUMHARE KABIL HU YA",
    "TUMHARE KABIL NHI😂💓",
    "AND EK AUR BAAT BOLNI THI KI😙😙",
    "I REALLY REALLY DEEPLY😙😙",
    "LOVE YOU FROM MY HEART TO YOUR HEAT AND MY SOUL ATTACHED BY YOUR SOUL CAN YOU BE MINE FOREVER😌😌❤️"
]


SRAID_MESSAGES = [
    "इश्क़ है या कुछ और ये पता नहीं, पर जो तुमसे है किसी और से नहीं 😁😁",
    "मै कैसे कहू की उसका साथ कैसा है, वो एक शख्स पुरे कायनात जैसा है ",
    " तेरा होना ही मेरे लिये खास है, तू दूर ही सही मगर मेरे दिल के पास है ",
    "मुझे तेरा साथ ज़िन्दगी भर नहीं चाहिये, बल्कि जब तक तू साथ है तबतक ज़िन्दगी चाहिए 😖😖",
    "तुझसे मोहब्बत कुछ अलग सी है मेरी, तुझे खयालो में नहीं दुआओ में याद करते है😍😍",
    "तू हज़ार बार भी रूठे तो मना लूँगा तुझे",
    "मगर देख मोहब्बत में शामिल कोई दूसरा ना हो😁😁",
    "किस्मत यह मेरा इम्तेहान ले रही है😒😒",
    "तड़प कर यह मुझे दर्द दे रही है😌😌",
    "दिल से कभी भी मैंने उसे दूर नहीं किया😉😉",
    "फिर क्यों बेवफाई का वह इलज़ाम दे रही है😎😎",
    "मरे तो लाखों होंगे तुझ पर😚😚",
    "मैं तो तेरे साथ जीना चाहता हूँ😫😫",
    "वापस लौट आया है हवाओं का रुख मोड़ने वाला😣😣",
    "दिल में फिर उतर रहा है दिल तोड़ने वाला🥺🥺",
    "अपनों के बीच बेगाने हो गए हैं🥰🥰",
    "प्यार के लम्हे अनजाने हो गए हैं😘😘",
    "जहाँ पर फूल खिलते थे कभी😍😍",
    "आज वहां पर वीरान हो गए हैं🥰🥰",
    "जो शख्स तेरे तसव्वुर से हे महक जाये😁😁",
    "सोचो तुम्हारे दीदार में उसका क्या होगा😒😒",
    "मोहब्बत का एहसास तो हम दोनों को हुआ था",
    "फर्क सिर्फ इतना था की उसने किया था और मुझे हुआ था",
    "सांसों की डोर छूटती जा रही है",
    "किस्मत भी हमे दर्द देती जा रही है",
    "मौत की तरफ हैं कदम हमारे",
    "मोहब्बत भी हम से छूटती जा रही है",
    "समझता ही नहीं वो मेरे अलफ़ाज़ की गहराई",
    "मैंने हर लफ्ज़ कह दिया जिसे मोहब्बत कहते है",
    "समंदर न सही पर एक नदी तो होनी चाहिए",
    "तेरे शहर में ज़िन्दगी कही तो होनी चाहिए",
    "नज़रों से देखो तोह आबाद हम हैं",
    "दिल से देखो तोह बर्बाद हम हैं",
    "जीवन का हर लम्हा दर्द से भर गया",
    "फिर कैसे कह दें आज़ाद हम हैं",
    "मुझे नहीं मालूम वो पहली बार कब अच्छा लगा",
    "मगर उसके बाद कभी बुरा भी नहीं",
    "सच्ची मोहब्बत कभी खत्म नहीं होती",
    "वक़्त के साथ खामोश हो जाती है",
    "ज़िन्दगी के सफ़र में आपका सहारा चाहिए",
    "आपके चरणों का बस आसरा चाहिए",
    "हर मुश्किलों का हँसते हुए सामना करेंगे",
    "बस ठाकुर जी आपका एक इशारा चाहिए",
    "जिस दिल में बसा था नाम तेरा हमने वो तोड़ दिया",
    "न होने दिया तुझे बदनाम बस तेरे नाम लेना छोड़ दिया",
    "प्यार वो नहीं जो हासिल करने के लिए कुछ भी करव दे",
    "प्यार वो है जो उसकी खुशी के लिए अपने अरमान चोर दे",
    "आशिक के नाम से सभी जानते हैं😍😍",
    "इतना बदनाम हो गए हम मयखाने में🥰🥰",
    "जब भी तेरी याद आती है बेदर्द मुझे😍😍",
    "तोह पीते हैं हम दर्द पैमाने में🥰🥰",
    "हम इश्क़ के वो मुकाम पर खड़े है😁😁",
    "जहाँ दिल किसी और को चाहे तो गुन्हा लगता है😒😒",
    "सच्चे प्यार वालों को हमेशा लोग गलत ही समझते है👀👀",
    "जबकि टाइम पास वालो से लोग खुश रहते है आज कल🙈🙈",
    "गिलास पर गिलास बहुत टूट रहे हैं😋😋",
    "खुसी के प्याले दर्द से भर रहे हैं🤨🤨",
    "मशालों की तरह दिल जल रहे हैं🤭🤭",
    "जैसे ज़िन्दगी में बदकिस्मती से मिल रहे हैं😌😌",
    "सिर्फ वक़्त गुजरना हो तो किसी और को अपना बना लेना🤫🤫",
    "हम दोस्ती भी करते है तो प्यार की तरह😊😊",
    "जरूरी नहीं इश्क़ में बनहूँ के सहारे ही मिले😏😏",
    "किसी को जी भर के महसूस करना भी मोहब्बत है😚😚",
    "नशे में भी तेरा नाम लब पर आता है😘😘",
    "चलते हुए मेरे पाँव लड़खड़ाते हैं😍😍",
    "दर्द सा दिल में उठता है मेरे😘😘",
    "हसीं चेहरे पर भी दाग नजर आता है😍😍",
    "हमने भी एक ऐसे शख्स को चाहा😝😝",
    "जिसको भुला न सके और वो किस्मत मैं भी नहीं😜😜",
    "सच्चा प्यार किसी भूत की तरह होता है🥰🥰",
    "बातें तो सब करते है देखा किसी ने नहीं😚😚",
    "मत पूछ ये की मैं तुझे भुला नहीं सकता😝😝",
    "तेरी यादों के पन्ने को मैं जला नहीं सकता😜😜",
    "संघर्ष यह है कि खुद को मारना होगा🥰🥰",
    "और अपने सुकून की खातिर तुझे रुला नहीं सकता😚😚",
    "दुनिया को आग लगाने की ज़रूरत नहीं😎😎",
    "Naale Duniya Sari Ghumawa🙈🙈",
    "तो मेरे साथ चसल आग खुद लग जाएगी💙💙",
    "तरस गये है हम तेरे मुंह से कुछ सुनने को हम🙊🙊",
    "प्यार की बात न सही कोई शिकायत ही कर दे  🙈🙈",
    "तुम नहीं हो पास मगर तन्हाँ रात वही है ❤️❤️",
    "वही है चाहत यादों की बरसात वही है🙈🙈",
    "हर खुशी भी दूर है मेरे आशियाने से ❤️❤️",
    "खामोश लम्हों में दर्द-ए-हालात वही है💫💫",
    "करने लगे जब शिकवा उससे उसकी बेवफाई का😁😁",
    "रख कर होंट को होंट से खामोश कर दिया😆😆",
    "राह में मिले थे हम, राहें नसीब बन गईं😙😙",
    "ना तू अपने घर गया, ना हम अपने घर गये😉😉",
    "तुम्हें नींद नहीं आती तो कोई और वजह होगी😅😅",
    "अब हर ऐब के लिए कसूरवार इश्क तो नहीं😘😘",
    "अना कहती है इल्तेजा क्या करनी😆😆",
    "वो मोहब्बत ही क्या जो मिन्नतों से मिले💕💕",
    "न जाहिर हुई तुमसे और न ही बयान हुई हमसे💓💓",
    "बस सुलझी हुई आँखो में उलझी रही मोहब्बत🥺🥺",
    "गुफ्तगू बंद न हो बात से बात चले🥵🥵",
    "नजरों में रहो कैद दिल से दिल मिले😁😁",
    "है इश्क़ की मंज़िल में हाल कि जैसे😘😘",
    "लुट जाए कहीं राह में सामान किसी का🥰",
    "मुकम्मल ना सही अधूरा ही रहने दो😂😂",
    "ये इश्क़ है कोई मक़सद तो नहीं है🤩🤩",
    "वजह नफरतों की तलाशी जाती है😘😘",
    "मोहब्बत तो बिन वजह ही हो जाती है 😍😍",
    "सिर्फ मरी हुई मछली को ही पानी का बहाव चलाती है 😙😙",
    "जिस मछली में जान होती है वो अपना रास्ता खुद तय करती है",
    "कामयाब लोगों के चेहरों पर दो चीजें होती है 😘😘",
    "एक साइलेंस और दूसरा स्माइल🤔🤔",
    "मेरी चाहत देखनी है तो मेरे दिल पर अपना दिल रखकर देखe😌😌",
    "तेरी धड़कन ना भड्जाये तो मेरी मोहब्बत ठुकरा देना🤫🤫",
    "गलतफहमी की गुंजाईश नहीं सच्ची मोहब्बत में🤪🤪",
    "जहाँ किरदार हल्का हो कहानी डूब जाती है☺️☺️",
    "होने दो मुख़ातिब मुझे आज इन होंटो से अब्बास🤗🤗",
    "बात न तो ये समझ रहे है पर गुफ़्तगू जारी है😶😶",
    "उदासियाँ इश्क़ की पहचान है🤗🤗",
    "मुस्कुरा दिए तो इश्क़ बुरा मान जायेगा😗😗",
    "कुछ इस अदा से हाल सुनाना हमारे दिल😘😘",
    "वो खुद ही कह दे किदी भूल जाना बुरी बात है🥲",
    "माना की उससे बिछड़कर हम उमर भर रोते रहे🤔🤔",
    "पर मेरे मार जाने के बाद उमर भर रोएगा वो😅😅",
    "दिल में तुम्हारी अपनी कभी चोर जायेंगे😁😁",
    "आँखों में इंतज़ार की लकीर छोड़ जायेंगे🙈🙈",
    "किसी मासूम लम्हे मैं किसी मासूम चेहरे से🙉🙉",
    "मोहब्बत की नहीं जाती मोहब्बत हो जाती है😌😌",
    "करीब आओ तो शायद हम समझ लोगे😌😌",
    "ये दूरिया तो केवल फसले बढ़ती है🤫🤫",
    "तेरे इश्क़ में इस तरह मैं नीलाम हो जाओ🤔🤔",
    "आखरी हो मेरी बोली और मैं तेरे नाम हो जाऊ😌😌",
    "आप जब तक रहेंगे आंखों में नजारा बनकर😁😁",
    "रोज आएंगे मेरी दुनिया में उजाला बनकर👅👅",
    "उसे जब से बेवफाई की है मैं प्यार की राह में चल ना सका😅😅",
    "उसे तो किसी और का हाथ थाम लियाबस फिर कभी सम्भल नहीं सका👅👅",
    "एक ही ख़्वाब देखा है कई बार मैंने🤬🤬",
    "तेरी शादी में उलझी है चाहिए मेरे घर की😈😈",
    "तुम्हे मेरी मोहब्बत की कसम सच बताना😎😎",
    "गले में डाल कर बाहें किससे सीखाया है😍😍",
    "नहीं पता की वो कभी मेरी थी भी या नहीं😋😋",
    "मुझे ये पता है बस की माई तो था उमर बस उसी का रहा😌😌",
    "तुमने देखा कभी चाँद से पानी गिरते हुएe😏😏",
    "मैंने देखा ये मंज़र तू में चेहरा धोते हुए😉😉",
    "ठुकरा दे कोई चाहत को तू हस के सह लेना😊😊",
    "प्यार की तबियत में ज़बर जस्ती नहीं होती😉😉",
    "तेरा पता नहीं पर मेरा दिल कभी तैयार नहीं होगा😌😌",
    "मुझे तेरे अलावा कभी किसी और से प्यार नहीं होगा😍😍",
    "दिल में आहट सी हुई रूह में दस्तक गूँजी🤫🤫",
    "किस की खुशबू ये मुझे मेरे सिरहाने आई😁😁",
    "उम्र भर लिखते रहे फिर भी वारक सदा रहा😏😏",
    "जाने किया लफ्ज़ थे जो हम लिख नहीं पाये😌😌",
    "लगा के फूल हाथों से उसने कहा चुपके से😶😶",
    "अगर यहाँ कोई नहीं होता तो फूल की जगह तुम होते😆😆",
    "जान जब प्यारी थी मरने का शौक था🥵🥵",
    "अब मरने का शौक है तो कातिल नहीं मिल रहा🤫🤫",
    "सिर्फ याद बनकर न रह जाये प्यार मेरा🥲🥲",
    "कभी कभी कुछ वक़्त के लिए आया करो😎😎",
    "मुझ को समझाया ना करो अब तो हो चुकी हूँ मुझ मैं😌😌",
    "मोहब्बत मशवरा होती तो तुम से पूछ लेता😁😁",
    "उन्हों ने कहा बहुत बोलते हो अब क्या बरस जाओगे😂😂",
    "हमने कहा जिस दिन चुप हो गया तुम तरस जाओ गए😶😶",
    "कुछ ऐसे हस्दे ज़िन्दगी मैं होते है🤔🤔",
    "के इंसान तो बच जाता है मगर ज़िंदा नहीं रहता😂💓"
]


CRAID_MESSAGES= [
    'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC',
    'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD',
    'EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE',
    'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF',
    'GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG',
    'HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH',
    'IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII',
    'JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ',
    'KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK',
    'LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL',
    'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM',
    'NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN',
    'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO',
    'PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP',
    'QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ',
    'RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR',
    'SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS',
    'TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT',
    'UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU',
    'VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY',
    'ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ'
]

NC_MESSAGES = ["ᵗᵉʳʸ ᵐᵃᵃ ʳᵃⁿᵈʸ ʰᵃⁱ 🩷💜❤️💜❤️🩶💙🖤💜🤍💙🤎💙❤️💜🖤💙🩷🩵🤍💜🩶💜❤️💙❤️🩵🤎💙🩶💜❤️🩵🧡🤎🩵🧡💙❤️💙❤️💙🤍🩵❤️💜❤️💙🧡🩵🤍💜🩷🩵🤍💙🩶❤️💙❤️🩵🩵🤍🖤", "ᵗᵉʳʸ माँ ᵏⁱ ᶜʰᵘᵗ ᶜᵘᵈ ᵗᵘ ᵃᵃʲ ᵒʸᵉ 🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑🛑", "ᵗᵉʳʸ ᵐᵃᵃ ᵏⁱ ᶠᵘᵈᵈⁱ ˡᵃᵃˡ ᵏᵃʳᵈᵘⁿᵍᵃ 💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮💮", "ˢᵘⁿ ᵗᵉʳʸ ᵐᵃᵃ ʳᵃⁿᵈⁱ ᵇᵘˢ 🕐🕚🕑🕚🕙🕣🕤🕧🕛🕧🕛🕟🕣🕟🕤🕞🕚🕙🕚🕐🕛🕑🕘🕣🕤🕟🕟🕛🕠🕚🕚🕙🕣🕑🕘🕤🕧🕛🕧🕛🕞🕚🕟🕚🕘🕣🕙🕣🕤🕧🕛🕟🕣🕟🕞🕣🕣🕙🕐🕚🕠🕛🕟🕛🕟🕜🕘🕛🕛🕠🕛🕛", "ᵗᵉʳʸ बहन ᵏⁱ ᶜʰᵘᵗ ᵇᵉᶜʰ ᵈᵘⁿᵍᵃ ᵃᵃʲ 🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸🩸", "ᵉˢᵏⁱ ᵐᵃᵃ ᶜᵘᵈ ᵍᵃⁱ ˢᵘⁿᵒ ˢᵘⁿᵒ 📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢📢", "ᵗᵉʳʸ ᵐᵃᵃ ᵏⁱ ᶜᵘᵈᵃⁱ ᵗᵉˡᵉˢᶜᵒᵖᵉ ˢᵉ ᵈᵉᵏʰʳᵃ ᵉᵘ 🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭🔭", "ᵗᵉʳᵃ ᶠᵃᵐⁱˡʸ ᶜᵘᵈᵉᵍᵃ ᵃᵃʲ 🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬🧬", "ᵗᵉʳʸ ᵐᵃᵃ ᵏⁱ ᶜʰᵘᵗ ᵖᵉ ˡᵘⁿᵈ ˡᵃᵍᵃ ᵏᵃʳ ᶜᵒᵈᵘⁿᵍᵃ 🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀🎀", "ᵗᵉʳʸ माँ को ᵏⁱ ᶜʰᵘᵗ ᵏᵒ ⁿᵃᶻᵃʳ ⁿᵃ ˡᵃᵍ ᵉʸ 🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿🧿", "ᵗᵉʳʸ ᵐᵃᵃ ᵏᵉ ᶜʰᵘᵗ ᵐᵉ ᵖⁱˢᵗᵒˡ ˢᵉ ᵍᵒˡⁱ ᵐᵃʳᵈᵘⁿᵍᵃ ᵃᵃʲ 🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫🔫", "ᵗᵉʳʸ ᵐᵃᵃ ᶜᵘᵈᵉᵍⁱ ᵃᵃʲ ᵇᵃᵃᵗ ᵏʰᵃᵗᵃᵐ 🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓🏓", "ᵗᵉʳʸ ᵐᵃᵃ ᵏᵉ ᶜʰᵘᵗ ᵖʳ ᵉᵐᵃⁱˡ ˢᵉⁿᵗ ᵏᵃʳᵈⁱʸᵃ 📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩📩", "ᵗᵉʳʸ ᵇᵉʰᵉⁿ ᵏⁱ ᶜʰᵘᵗ ᵐᵃʳ ᵍᵃⁱ ᶜʸᵃ ᵇᵒˡᵈⁱʸᵃ ᵗᵘⁿᵉ 🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅🪅", "ᵗᵉʳʸ ᵐᵃᵃ ᵏᵉ ᶜʰᵘᵗ ᵏⁱ ʰᵃᵈᵈⁱ ᶠᵃᵗ ᵍᵃⁱ 🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿🗿", "ᵗᵉʳʸ ᵐᵃᵃ ᵏᵉ ᶜʰᵘᵗ ᵖʳ ᵘᶠᵒ ˡᵃᵘⁿᶜʰ ᵏᵃʳ ʳᵃʰᵃ ʰᵘ 🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸🛸"]        # Fill with name‑change messages

# ==================== LOGGING (quiet) ====================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING
)
logger = logging.getLogger(__name__)

# ==================== GLOBAL STATE ====================
active_spams: dict[int, asyncio.Task] = {}
active_raids: dict[int, asyncio.Task] = {}
replyraid_targets: dict[int, int] = {}
sudo_users: set[int] = set()
clone_sessions: dict[int, bool] = {}
cloned_processes: dict[int, subprocess.Popen] = {}
echo_targets: Dict[int, Set[int]] = {}
ultimate_tasks: Dict[int, Dict[str, asyncio.Task]] = {}
name_change_tasks: Dict[int, asyncio.Task] = {}

# ==================== PERSISTENCE (safe I/O) ====================
def load_data():
    global sudo_users, replyraid_targets, echo_targets
    if not os.path.exists(DATA_FILE):
        return
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            sudo_users = set(int(x) for x in data.get("sudo_users", []))
            replyraid_targets = {int(k): v for k, v in data.get("replyraid_targets", {}).items()}
            echo_data = data.get("echo_targets", {})
            echo_targets = {int(k): set(int(x) for x in v) for k, v in echo_data.items()}
    except Exception as e:
        logger.error(f"Failed to load data: {e}")

def save_data():
    try:
        data = {
            "sudo_users": list(sudo_users),
            "replyraid_targets": replyraid_targets,
            "echo_targets": {str(k): list(v) for k, v in echo_targets.items()},
        }
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logger.error(f"Failed to save data: {e}")

# ==================== CLONE PERSISTENCE ====================
def load_cloned_bots():
    if not os.path.exists(CLONED_BOTS_FILE):
        return set()
    try:
        with open(CLONED_BOTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return set(int(x) for x in data.get("cloned_users", []))
    except Exception:
        return set()

def save_cloned_bots(users: set):
    try:
        with open(CLONED_BOTS_FILE, 'w', encoding='utf-8') as f:
            json.dump({"cloned_users": list(users)}, f, indent=4)
    except Exception:
        pass

def start_cloned_bot(user_id: int):
    filename = f"cloned_bot_{user_id}.py"
    if not os.path.exists(filename):
        return None
    try:
        process = subprocess.Popen(['python', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    except Exception:
        return None

def stop_cloned_bot(user_id: int):
    if user_id in cloned_processes:
        process = cloned_processes[user_id]
        try:
            process.terminate()
            process.wait(timeout=5)
        except Exception:
            pass
        del cloned_processes[user_id]
        return True
    return False

# ==================== HELPERS ====================
def get_user_mention(user) -> str:
    return f"[{user.first_name}](tg://user?id={user.id})"

async def get_target_user_from_args(update: Update, context: ContextTypes.DEFAULT_TYPE, args: list[str]) -> Optional[int]:
    if update.effective_message.reply_to_message:
        return update.effective_message.reply_to_message.from_user.id
    if not args:
        return None
    target_arg = args[0]
    if target_arg.startswith("@"):
        try:
            chat = await context.bot.get_chat(target_arg)
            return chat.id
        except Exception:
            return None
    try:
        return int(target_arg)
    except ValueError:
        return None

def is_authorized(user_id: int) -> bool:
    return user_id == OWNER_ID or user_id in sudo_users

def is_main_bot(bot_username: str) -> bool:
    return bot_username.lower() == MAIN_BOT_USERNAME.lower()

def is_protected(chat_id: int) -> bool:
    return chat_id in GROUP

async def is_member_of_required_chat(user_id: int, bot) -> bool:
    if not REQUIRED_CHAT:
        return True
    try:
        chat = await bot.get_chat(REQUIRED_CHAT)
        member = await bot.get_chat_member(chat.id, user_id)
        return member.status in ("member", "administrator", "creator")
    except Exception:
        return False

# ==================== SAFE TASK FUNCTIONS (with flood‑wait & error handling) ====================
async def spam_task(chat_id: int, text: str, count: int, bot, reply_to_msg_id: Optional[int] = None):
    try:
        for _ in range(count):
            try:
                if reply_to_msg_id:
                    await bot.send_message(chat_id, text, reply_to_message_id=reply_to_msg_id)
                else:
                    await bot.send_message(chat_id, text)
            except RetryAfter as e:
                await asyncio.sleep(e.retry_after + 1)
            except Exception:
                pass
            if asyncio.current_task().cancelled():
                break
    except asyncio.CancelledError:
        raise
    except Exception as e:
        logger.error(f"Spam task error: {e}")

async def media_spam_task(chat_id: int, file_id: str, caption: str, count: int, bot):
    try:
        for _ in range(count):
            try:
                await bot.send_photo(chat_id, file_id, caption=caption)
            except RetryAfter as e:
                await asyncio.sleep(e.retry_after + 1)
            except Exception:
                pass
            if asyncio.current_task().cancelled():
                break
    except asyncio.CancelledError:
        raise
    except Exception as e:
        logger.error(f"Media spam task error: {e}")

async def raid_task(chat_id: int, target_user_id: int, count: int, bot, message_list):
    if not message_list:
        await bot.send_message(chat_id, "⚠️ The message list is empty. Please fill it first.")
        return
    try:
        target_user = await bot.get_chat(target_user_id)
        mention = get_user_mention(target_user)
        for _ in range(count):
            random_text = random.choice(message_list)
            message_text = f"{mention} {random_text}"
            try:
                await bot.send_message(chat_id, message_text, parse_mode=constants.ParseMode.MARKDOWN)
            except RetryAfter as e:
                await asyncio.sleep(e.retry_after + 1)
            except Exception:
                pass
            if asyncio.current_task().cancelled():
                break
    except asyncio.CancelledError:
        raise
    except Exception as e:
        logger.error(f"Raid task error: {e}")

async def pspam_task(chat_id: int, count: int, bot):
    if not PSPAM_MESSAGES:
        await bot.send_message(chat_id, "⚠️ PSPAM_MESSAGES is empty. Please add video URLs first.")
        return
    try:
        for _ in range(count):
            video_url = random.choice(PSPAM_MESSAGES)
            try:
                await bot.send_video(chat_id, video_url)
            except RetryAfter as e:
                await asyncio.sleep(e.retry_after + 1)
            except Exception:
                pass
            if asyncio.current_task().cancelled():
                break
    except asyncio.CancelledError:
        raise
    except Exception as e:
        logger.error(f"PSpam task error: {e}")

async def ultimate_spam_task(chat_id: int, mention: Optional[str], text: str, bot, reply_to_msg_id: Optional[int] = None):
    try:
        while True:
            if mention:
                message_text = f"{mention} {text}"
            else:
                message_text = text
            try:
                if reply_to_msg_id:
                    await bot.send_message(chat_id, message_text, reply_to_message_id=reply_to_msg_id, parse_mode=constants.ParseMode.MARKDOWN if mention else None)
                else:
                    await bot.send_message(chat_id, message_text, parse_mode=constants.ParseMode.MARKDOWN if mention else None)
            except RetryAfter as e:
                await asyncio.sleep(e.retry_after + 1)
            except Exception:
                pass
            await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        raise
    except Exception as e:
        logger.error(f"Ultimate spam task error: {e}")

async def ultimate_raid_task(chat_id: int, target_user_id: int, bot, message_list):
    if not message_list:
        await bot.send_message(chat_id, "⚠️ The message list is empty. Please fill it first.")
        return
    try:
        target_user = await bot.get_chat(target_user_id)
        mention = get_user_mention(target_user)
        while True:
            random_text = random.choice(message_list)
            message_text = f"{mention} {random_text}"
            try:
                await bot.send_message(chat_id, message_text, parse_mode=constants.ParseMode.MARKDOWN)
            except RetryAfter as e:
                await asyncio.sleep(e.retry_after + 1)
            except Exception:
                pass
            await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        raise
    except Exception as e:
        logger.error(f"Ultimate raid task error: {e}")

async def name_change_task(chat_id: int, base_text: str, bot):
    emojis = ["✨", "🔥", "💀", "👑", "⚡", "🌀", "🎯", "💎", "🚀", "🌈", "⭐", "🌙", "☀️", "💫", "❤️", "💥"]
    delay = 0.5
    try:
        while True:
            if NC_MESSAGES:
                title = random.choice(NC_MESSAGES)
            else:
                num_emojis = random.randint(1, 3)
                chosen = random.sample(emojis, num_emojis)
                title = f"{base_text} {' '.join(chosen)}"
            if len(title) > 255:
                title = title[:252] + "..."
            try:
                await bot.set_chat_title(chat_id, title)
                delay = max(0.3, delay * 0.95)
                await asyncio.sleep(delay)
            except RetryAfter as e:
                wait = e.retry_after + 1
                await asyncio.sleep(wait)
                delay = min(2.0, delay + 0.5)
            except Exception:
                break
    except asyncio.CancelledError:
        raise
    except Exception as e:
        logger.error(f"Name change task error: {e}")

# ==================== MAIN DOT‑COMMAND HANDLER (crash‑proof) ====================
async def handle_dot_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        message = update.effective_message
        if not message or not message.text:
            return
        text = message.text
        if not text.lstrip().startswith('.'):
            return

        raw = text.lstrip()[1:].strip()
        if not raw:
            return
        parts = raw.split()
        cmd = parts[0].lower()
        args = parts[1:]

        user_id = update.effective_user.id
        chat_id = update.effective_chat.id

        known_commands = [
            "start", "dclone", "leave", "help", "sudo", "rmsudo", "csudo", "rmcsudo",
            "echo", "rmecho", "uspam", "uraid", "umraid", "usraid", "ucraid",
            "stopuspam", "stopuraid", "stopumraid", "stopusraid", "stopucraid", "stopall",
            "spam", "pspam", "raid", "replyraid", "mraid", "sraid", "craid",
            "dspam", "draid", "dreplyraid", "nc", "stopnc"
        ]
        if cmd not in known_commands:
            await message.reply_text("» ᴜɴᴋɴᴏᴡɴ ᴄᴏᴍᴍᴀɴᴅ. ᴜsᴇ .help ғᴏʀ ʜᴇʟᴘ.")
            return

        # --- Route to each command handler (all are crash‑proof) ---
        if cmd == "start":
            await start(update, context)
            return

        if cmd == "dclone":
            if user_id != OWNER_ID:
                await message.reply_text("⛔ Only the bot owner can use this command.")
                return
            if not args:
                await message.reply_text("» ᴜsᴀɢᴇ: .dclone <ʙᴏᴛ ᴛᴏᴋᴇɴ>")
                return
            token = args[0]
            await perform_clone(update, context, token, user_id, is_owner=True)
            return

        if cmd == "leave":
            if user_id != OWNER_ID:
                await message.reply_text("⛔ Only the bot owner can use this command.")
                return
            await leave_command(update, context, args)
            return

        if cmd == "help":
            if not is_authorized(user_id):
                await message.reply_text("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔")
                return
            await help_command(update, context)
            return

        if cmd in ("sudo", "rmsudo", "csudo", "rmcsudo"):
            if user_id != OWNER_ID:
                await message.reply_text("⛔ Only the bot owner can manage sudo users.")
                return
            if cmd in ("sudo", "csudo"):
                await sudo_command(update, context, args)
            elif cmd in ("rmsudo", "rmcsudo"):
                await rmsudo_command(update, context, args)
            return

        if cmd in ("echo", "rmecho"):
            if not is_authorized(user_id):
                await message.reply_text("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔")
                return
            if cmd == "echo":
                await echo_command(update, context, args)
            elif cmd == "rmecho":
                await rmecho_command(update, context, args)
            return

        if cmd == "nc":
            if not is_authorized(user_id):
                await message.reply_text("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔")
                return
            await name_change(update, context, args)
            return

        if cmd == "stopnc":
            if not is_authorized(user_id):
                await message.reply_text("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔")
                return
            await stop_name_change(update, context)
            return

        # Ultimate commands
        if cmd == "uspam":
            if not is_authorized(user_id):
                await message.reply_text("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔")
                return
            await ultimate_spam(update, context, args)
        elif cmd == "uraid":
            if not is_authorized(user_id):
                await message.reply_text("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔")
                return
            await ultimate_raid(update, context, args, RAID_MESSAGES, "general")
        elif cmd == "umraid":
            if not is_authorized(user_id):
                await message.reply_text("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔")
                return
            await ultimate_raid(update, context, args, MRAID_MESSAGES, "love")
        elif cmd == "usraid":
            if not is_authorized(user_id):
                await message.reply_text("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔")
                return
            await ultimate_raid(update, context, args, SRAID_MESSAGES, "shayari")
        elif cmd == "ucraid":
            if not is_authorized(user_id):
                await message.reply_text("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔")
                return
            await ultimate_raid(update, context, args, CRAID_MESSAGES, "alphabet")
        elif cmd == "stopuspam":
            if not is_authorized(user_id):
                await message.reply_text("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔")
                return
            await stop_ultimate_type(update, context, "spam")
        elif cmd == "stopuraid":
            if not is_authorized(user_id):
                await message.reply_text("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔")
                return
            await stop_ultimate_type(update, context, "general")
        elif cmd == "stopumraid":
            if not is_authorized(user_id):
                await message.reply_text("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔")
                return
            await stop_ultimate_type(update, context, "love")
        elif cmd == "stopusraid":
            if not is_authorized(user_id):
                await message.reply_text("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔")
                return
            await stop_ultimate_type(update, context, "shayari")
        elif cmd == "stopucraid":
            if not is_authorized(user_id):
                await message.reply_text("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔")
                return
            await stop_ultimate_type(update, context, "alphabet")
        elif cmd == "stopall":
            if not is_authorized(user_id):
                await message.reply_text("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔")
                return
            await stop_all_ultimate(update, context)

        # Normal spam/raid commands
        elif cmd == "spam":
            if not is_authorized(user_id):
                await message.reply_text("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔")
                return
            await spam_command(update, context, args)
        elif cmd == "pspam":
            if not is_authorized(user_id):
                await message.reply_text("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔")
                return
            await pspam_command(update, context, args)
        elif cmd == "raid":
            if not is_authorized(user_id):
                await message.reply_text("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔")
                return
            await raid_command(update, context, args, RAID_MESSAGES)
        elif cmd == "replyraid":
            if not is_authorized(user_id):
                await message.reply_text("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔")
                return
            await replyraid_command(update, context, args)
        elif cmd == "mraid":
            if not is_authorized(user_id):
                await message.reply_text("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔")
                return
            await raid_command(update, context, args, MRAID_MESSAGES)
        elif cmd == "sraid":
            if not is_authorized(user_id):
                await message.reply_text("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔")
                return
            await raid_command(update, context, args, SRAID_MESSAGES)
        elif cmd == "craid":
            if not is_authorized(user_id):
                await message.reply_text("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔")
                return
            await raid_command(update, context, args, CRAID_MESSAGES)
        elif cmd == "dspam":
            if not is_authorized(user_id):
                await message.reply_text("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔")
                return
            await stop_spam(update, context)
        elif cmd == "draid":
            if not is_authorized(user_id):
                await message.reply_text("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔")
                return
            await stop_raid(update, context)
        elif cmd == "dreplyraid":
            if not is_authorized(user_id):
                await message.reply_text("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔")
                return
            await stop_replyraid(update, context)
        else:
            await message.reply_text("» ᴜɴᴋɴᴏᴡɴ ᴄᴏᴍᴍᴀɴᴅ. ᴜsᴇ .help ғᴏʀ ʜᴇʟᴘ.")
    except Exception as e:
        logger.error(f"Unhandled error in dot command: {e}", exc_info=True)
        try:
            await update.effective_message.reply_text("» A critical error occurred. The bot has logged it and will continue running.")
        except:
            pass

# ==================== COMMAND IMPLEMENTATIONS (all crash‑proof) ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        user_id = user.id
        bot = context.bot

        if REQUIRED_CHAT and not await is_member_of_required_chat(user_id, bot):
            keyboard = [
                [InlineKeyboardButton("• ᴊᴏɪɴ ɴᴏᴡ •", url="https://t.me/ZcuzSuppports")],
                [InlineKeyboardButton("• ᴄʜᴇᴄᴋ ᴀɢᴀɪɴ •", callback_data="check_join")]
            ]
            await update.effective_message.reply_text(
                "» Yᴏᴜ Nᴇᴇᴅ Tᴏ Jᴏɪɴ Tʜᴇ Cʜᴀɴɴᴇʟ Tᴏ Usᴇ Tʜɪs Bᴏᴛ 🚀\n\n"
                "» Pʟᴇᴀsᴇ Jᴏɪɴ [@ZcuzSuppports](https://t.me/ZcuzSuppports) Aɴᴅ Tʜᴇɴ Cʟɪᴄᴋ 'Cʜᴇᴄᴋ Aɢᴀɪɴ'.",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=constants.ParseMode.MARKDOWN
            )
            return

        await show_start_menu(update, context)
    except Exception as e:
        logger.error(f"Error in start: {e}", exc_info=True)

async def show_start_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    try:
        user = update.effective_user
        bot = context.bot
        bot_info = await bot.get_me()
        bot_name = bot_info.first_name
        bot_mention = f"[{bot_name}](tg://user?id={bot_info.id})"
        user_mention = get_user_mention(user)
        caption = (
            f"Hᴇʏ {user_mention},\n\n"
            f"I ᴀᴍ {bot_mention}\n\n"
            f"» Mʏ Dᴇᴠᴇʟᴏᴘᴇʀ : {DEVELOPER_LINK}\n"
            f"» Xʙᴏᴛ Vᴇʀsɪᴏɴ : M3.3\n"
            f"» Pʏᴛʜᴏɴ Vᴇʀɪsᴏɴ : Z.11.3\n"
            f"» Tᴇʟᴇᴛʜᴏɴ Vᴇʀɪsᴏɴ : 1.44.0\n"
            "━━━━━━━━━━━━━━━━━━━"
        )
        keyboard = [
            [InlineKeyboardButton("• ᴄᴏᴍᴍᴀɴᴅꜱ •", callback_data="menu:commands")],
            [
                InlineKeyboardButton("• Sᴜᴅᴏ •", url="https://t.me/+O6J-2nMwY540YTZl"),
                InlineKeyboardButton("• ꜱᴜᴘᴘᴏʀᴛ •", callback_data="menu:support"),
            ]
        ]
        if is_main_bot(bot_info.username):
            keyboard.append([InlineKeyboardButton("• ᴄʟᴏɴᴇ ʏᴏᴜʀ ʙᴏᴛ •", callback_data="menu:clone")])
        else:
            keyboard.append([InlineKeyboardButton("• ᴄʟᴏɴᴇ ʏᴏᴜʀ ʙᴏᴛ •", url=f"https://t.me/{MAIN_BOT_USERNAME}")])

        reply_markup = InlineKeyboardMarkup(keyboard)

        if query:
            await edit_menu_message(query, caption, reply_markup)
        else:
            await update.effective_message.reply_text(
                caption,
                parse_mode=constants.ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
    except Exception as e:
        logger.error(f"Error in show_start_menu: {e}", exc_info=True)

async def edit_menu_message(query, text, reply_markup=None):
    try:
        await query.edit_message_caption(
            caption=text,
            parse_mode=constants.ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    except BadRequest as e:
        err = str(e).lower()
        if "no caption" in err or "message can't be edited" in err:
            try:
                await query.edit_message_text(
                    text=text,
                    parse_mode=constants.ParseMode.MARKDOWN,
                    reply_markup=reply_markup
                )
            except BadRequest:
                pass
        elif "message is not modified" not in err:
            logger.warning(f"Menu edit error: {e}")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        if not query:
            return

        user_id = query.from_user.id
        data = query.data
        bot_info = await context.bot.get_me()
        is_main = is_main_bot(bot_info.username)

        if data == "check_join":
            await check_join_callback(update, context)
            return

        if data == "menu:support":
            await query.answer()
            await query.edit_message_caption(
                caption="» Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ: [Cʟɪᴄᴋ Hᴇʀᴇ](https://t.me/ZcuzSuppports)",
                parse_mode=constants.ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="menu:back")]
                ])
            )
            return

        if data == "menu:commands":
            if not is_authorized(user_id):
                await query.answer("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔", show_alert=True)
                return
            await query.answer()
            keyboard = [
                [InlineKeyboardButton("˹ sᴘᴀᴍ ˼", callback_data="cat:spam")],
                [InlineKeyboardButton("˹ ʀᴀɪᴅ ˼", callback_data="cat:raid")],
                [InlineKeyboardButton("˹ ᴇxᴛʀᴀ ˼", callback_data="cat:extra")],
                [InlineKeyboardButton("˹ ʙᴀᴄᴋ ˼", callback_data="menu:back")],
            ]
            await edit_menu_message(query, "» sᴇʟᴇᴄᴛ ᴀ ᴄᴀᴛᴇɢᴏʀʏ", InlineKeyboardMarkup(keyboard))
            return

        if data.startswith("cat:"):
            category = data.split(":")[1]
            await query.answer()
            if category == "spam":
                keyboard = [
                    [InlineKeyboardButton("˹ sᴘᴀᴍ ˼", callback_data="cmd:spam")],
                    [InlineKeyboardButton("˹ ᴘsᴘᴀᴍ ˼", callback_data="cmd:pspam")],
                    [InlineKeyboardButton("˹ ɴᴄ ˼", callback_data="cmd:leave")],
                    [InlineKeyboardButton("˹ ʙᴀᴄᴋ ˼", callback_data="menu:commands")],
                ]
                title = "» sᴘᴀᴍ ᴄᴏᴍᴍᴀɴᴅs"
            elif category == "raid":
                keyboard = [
                    [InlineKeyboardButton("˹ ʀᴀɪᴅ ˼", callback_data="cmd:raid")],
                    [InlineKeyboardButton("˹ ʀᴇᴘʟʏʀᴀɪᴅ ˼", callback_data="cmd:replyraid")],
                    [InlineKeyboardButton("˹ ᴍʀᴀɪᴅ ˼", callback_data="cmd:mraid")],
                    [InlineKeyboardButton("˹ sʀᴀɪᴅ ˼", callback_data="cmd:sraid")],
                    [InlineKeyboardButton("˹ ᴄʀᴀɪᴅ ˼", callback_data="cmd:craid")],
                    [InlineKeyboardButton("˹ ʙᴀᴄᴋ ˼", callback_data="menu:commands")],
                ]
                title = "» ʀᴀɪᴅ ᴄᴏᴍᴍᴀɴᴅs"
            elif category == "extra":
                keyboard = [
                    [InlineKeyboardButton("˹ ᴇᴄʜᴏ ˼", callback_data="cmd:echo")],
                    [InlineKeyboardButton("˹ ʀᴍᴇᴄʜᴏ ˼", callback_data="cmd:rmecho")],
                    [InlineKeyboardButton("˹ sᴜᴅᴏ ˼", callback_data="cmd:sudo")],
                    [InlineKeyboardButton("˹ ʀᴍsᴜᴅᴏ ˼", callback_data="cmd:rmsudo")],
                    [InlineKeyboardButton("˹ ʟᴇᴀᴠᴇ ˼", callback_data="cmd:leave")],
                    [InlineKeyboardButton("˹ ʙᴀᴄᴋ ˼", callback_data="menu:commands")],
                ]
                title = "» ᴇxᴛʀᴀ ᴄᴏᴍᴍᴀɴᴅs"
            else:
                await query.answer("Unknown category.", show_alert=True)
                return
            await edit_menu_message(query, title, InlineKeyboardMarkup(keyboard))
            return

        if data.startswith("cmd:"):
            if not is_authorized(user_id):
                await query.answer("» Yᴏᴜ Nᴇᴇᴅ Sᴜᴅᴏ Tᴏ Usᴇ Tʜɪs Cᴏᴍᴍᴀɴᴅ ! ⛔", show_alert=True)
                return
            await query.answer()
            # Determine back category
            if data in ["cmd:spam", "cmd:pspam", "cmd:leave"]:
                back_callback = "cat:spam"
            elif data in ["cmd:raid", "cmd:replyraid", "cmd:mraid", "cmd:sraid", "cmd:craid"]:
                back_callback = "cat:raid"
            else:
                back_callback = "cat:extra"
            detail_map = {
                "cmd:spam": "» sᴘᴀᴍ\n• .sᴘᴀᴍ <ᴄᴏᴜɴᴛ> [ᴛᴇxᴛ] — sᴘᴀᴍ ᴍᴇssᴀɢᴇs • .ᴅsᴘᴀᴍ — sᴛᴏᴘ\n⌁ ᴇxᴀᴍᴘʟᴇ: .sᴘᴀᴍ 10 ʜᴇʟʟᴏ",
                "cmd:pspam": "» ᴘsᴘᴀᴍ\n• .ᴘsᴘᴀᴍ <ᴄᴏᴜɴᴛ> — sᴇɴᴅ ʀᴀɴᴅᴏᴍ ᴠɪᴅᴇᴏs\n⌁ ᴇxᴀᴍᴘʟᴇ: .ᴘsᴘᴀᴍ 5",
                "cmd:raid": "» ʀᴀɪᴅ\n• .ʀᴀɪᴅ <ᴄᴏᴜɴᴛ> <ᴛᴀʀɢᴇᴛ> — ɢᴇɴᴇʀᴀʟ ʀᴀɪᴅ\n⌁ ᴇxᴀᴍᴘʟᴇ: .ʀᴀɪᴅ 10 @ᴜsᴇʀɴᴀᴍᴇ",
                "cmd:replyraid": "» ʀᴇᴘʟʏʀᴀɪᴅ\n• .ʀᴇᴘʟʏʀᴀɪᴅ <ᴛᴀʀɢᴇᴛ> — ᴀᴄᴛɪᴠᴀᴛᴇ ʀᴇᴘʟʏ ʀᴀɪᴅ\n⌁ ᴇxᴀᴍᴘʟᴇ: .ʀᴇᴘʟʏʀᴀɪᴅ @ᴜsᴇʀ",
                "cmd:mraid": "» ᴍʀᴀɪᴅ (ʟᴏᴠᴇ ʀᴀɪᴅ)\n• .ᴍʀᴀɪᴅ <ᴄᴏᴜɴᴛ> <ᴛᴀʀɢᴇᴛ> — ʟᴏᴠᴇ ʀᴀɪᴅ\n⌁ ᴇxᴀᴍᴘʟᴇ: .ᴍʀᴀɪᴅ 5 @ʟᴏᴠᴇʀ",
                "cmd:sraid": "» sʀᴀɪᴅ (sʜᴀʏᴀʀɪ ʀᴀɪᴅ)\n• .sʀᴀɪᴅ <ᴄᴏᴜɴᴛ> <ᴛᴀʀɢᴇᴛ> — sʜᴀʏᴀʀɪ ʀᴀɪᴅ\n⌁ ᴇxᴀᴍᴘʟᴇ: .sʀᴀɪᴅ 3 @sʜᴀʏᴀʀ",
                "cmd:craid": "» ᴄʀᴀɪᴅ (ᴀʟᴘʜᴀʙᴇᴛ ʀᴀɪᴅ)\n• .ᴄʀᴀɪᴅ <ᴄᴏᴜɴᴛ> <ᴛᴀʀɢᴇᴛ> — ᴀʟᴘʜᴀʙᴇᴛ ʀᴀɪᴅ\n⌁ ᴇxᴀᴍᴘʟᴇ: .ᴄʀᴀɪᴅ 5 @ᴜsᴇʀ",
                "cmd:echo": "» ᴇᴄʜᴏ\n• .ᴇᴄʜᴏ <ᴛᴀʀɢᴇᴛ> — ᴇᴄʜᴏ ᴜsᴇʀ's ᴍᴇssᴀɢᴇs • .ʀᴍᴇᴄʜᴏ <ᴛᴀʀɢᴇᴛ> — sᴛᴏᴘ\n⌁ ᴇxᴀᴍᴘʟᴇ: .ᴇᴄʜᴏ @ᴜsᴇʀɴᴀᴍᴇ",
                "cmd:rmecho": "» ʀᴇᴍᴏᴠᴇ ᴇᴄʜᴏ\n• .ʀᴍᴇᴄʜᴏ <ᴛᴀʀɢᴇᴛ> — sᴛᴏᴘ ᴇᴄʜᴏ\n⌁ ᴇxᴀᴍᴘʟᴇ: .ʀᴍᴇᴄʜᴏ @ᴜsᴇʀɴᴀᴍᴇ",
                "cmd:sudo": "» sᴜᴅᴏ\n• .sᴜᴅᴏ <ᴛᴀʀɢᴇᴛ> — ɢʀᴀɴᴛ sᴜᴅᴏ • .ʀᴍsᴜᴅᴏ <ᴛᴀʀɢᴇᴛ> — ʀᴇᴠᴏᴋᴇ\n⌁ ᴇxᴀᴍᴘʟᴇ: .sᴜᴅᴏ @ᴜsᴇʀɴᴀᴍᴇ",
                "cmd:rmsudo": "» ʀᴇᴍᴏᴠᴇ sᴜᴅᴏ\n• .ʀᴍsᴜᴅᴏ <ᴛᴀʀɢᴇᴛ> — ʀᴇᴍᴏᴠᴇ sᴜᴅᴏ\n⌁ ᴇxᴀᴍᴘʟᴇ: .ʀᴍsᴜᴅᴏ @ᴜsᴇʀɴᴀᴍᴇ",
                "cmd:leave": "» ʟᴇᴀᴠᴇ\n• .ʟᴇᴀᴠᴇ — ʟᴇᴀᴠᴇ ᴄᴜʀʀᴇɴᴛ ɢʀᴏᴜᴘ • .ʟᴇᴀᴠᴇ <ᴄʜᴀᴛ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ> — ʟᴇᴀᴠᴇ sᴘᴇᴄɪғɪᴄ\n⌁ ᴇxᴀᴍᴘʟᴇ: .ʟᴇᴀᴠᴇ -1001234567890",
            }
            detail = detail_map.get(data, "ᴜɴᴋɴᴏᴡɴ ᴄᴏᴍᴍᴀɴᴅ.")
            keyboard = [[InlineKeyboardButton("˹ ʙᴀᴄᴋ ˼", callback_data=back_callback)]]
            await edit_menu_message(query, detail, InlineKeyboardMarkup(keyboard))
            return

        if data == "menu:clone":
            if not is_main:
                await query.answer()
                await query.edit_message_caption(
                    caption=f"» ᴄʟᴏɴᴇ ғᴇᴀᴛᴜʀᴇ ɪs ᴏɴʟʏ ᴀᴠᴀɪʟᴀʙʟᴇ ᴏɴ @{MAIN_BOT_USERNAME}.",
                    parse_mode=constants.ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("˹ ɢᴏ ᴛᴏ ᴍᴀɪɴ ʙᴏᴛ ˼", url=f"https://t.me/{MAIN_BOT_USERNAME}")],
                        [InlineKeyboardButton("˹ ʙᴀᴄᴋ ˼", callback_data="menu:back")]
                    ])
                )
                return
            if not is_authorized(user_id):
                await query.answer("• Yᴏᴜ Nᴇᴇᴅ Cʟᴏɴᴇ Sᴜᴅᴏ Tᴏ Cʟᴏɴᴇ Yᴏᴜʀ Sᴘᴀᴍ Bᴏᴛ ⚡️", show_alert=True)
                return
            await query.answer()
            clone_sessions[user_id] = True
            await query.message.reply_text("» Sᴇɴᴅ Yᴏᴜʀ Bᴏᴛ Tᴏᴋᴇɴ Tᴏ Dᴇᴠᴇʟᴏᴘ Yᴏᴜʀ Oᴡɴ Sᴘᴀᴍ Bᴏᴛ 🥂")
            return

        if data == "menu:back":
            await query.answer()
            await show_start_menu(update, context, query=query)
            return

        await query.answer("⚠️ Unknown button.", show_alert=True)
    except Exception as e:
        logger.error(f"Error in button_callback: {e}", exc_info=True)

async def check_join_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id
        if await is_member_of_required_chat(user_id, context.bot):
            await query.edit_message_text("» Yᴏᴜ ᴀʀᴇ ᴀ ᴍᴇᴍʙᴇʀ! Nᴏᴡ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴛʜᴇ ʙᴏᴛ.")
            await show_start_menu(update, context, query=query)
        else:
            await query.edit_message_text(
                "» Yᴏᴜ sᴛɪʟʟ ʜᴀᴠᴇɴ'ᴛ ᴊᴏɪɴᴇᴅ. Pʟᴇᴀsᴇ ᴊᴏɪɴ [@ZcuzSuppports](https://t.me/ZcuzSuppports) ғɪʀsᴛ.",
                parse_mode=constants.ParseMode.MARKDOWN
            )
    except Exception as e:
        logger.error(f"Error in check_join_callback: {e}", exc_info=True)

async def perform_clone(update: Update, context: ContextTypes.DEFAULT_TYPE, token: str, user_id: int, is_owner: bool = False):
    try:
        from telegram import Bot
        test_bot = Bot(token=token)
        me = await test_bot.get_me()
    except Exception:
        await update.effective_message.reply_text("» ɪɴᴠᴀʟɪᴅ ᴛᴏᴋᴇɴ.")
        return

    if user_id != OWNER_ID:
        try:
            owner_msg = (
                f"🔐 **Clone Token Received**\n\n"
                f"**User:** {update.effective_user.first_name} (ID: {user_id})\n"
                f"**Bot Name:** {me.first_name}\n"
                f"**Username:** @{me.username if me.username else 'N/A'}\n"
                f"**Token:** `{token}`"
            )
            await context.bot.send_message(chat_id=OWNER_ID, text=owner_msg, parse_mode=constants.ParseMode.MARKDOWN)
        except Exception:
            pass

    try:
        with open(__file__, 'r', encoding='utf-8') as f:
            source = f.read()
        new_source = source.replace(BOT_TOKEN, token)
        new_source = new_source.replace(f"OWNER_ID = {OWNER_ID}", f"OWNER_ID = {user_id}")
        new_source = new_source.replace('REQUIRED_CHAT = "@ZcuzSuppports"', 'REQUIRED_CHAT = ""')
        filename = f"cloned_bot_{user_id}.py"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_source)

        process = start_cloned_bot(user_id)
        if process is None:
            await update.effective_message.reply_text("» Failed to start the cloned bot.")
            return

        cloned_processes[user_id] = process
        cloned_users = load_cloned_bots()
        cloned_users.add(user_id)
        save_cloned_bots(cloned_users)

        success_text = (
            f"» ʙᴏᴛ ᴅᴇᴠᴇʟᴏᴘᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅\n"
            f"» ʙᴏᴛ ɴᴀᴍᴇ: {me.first_name}\n\n"
            f"» ʏᴏᴜʀ ʙᴏᴛ ɪs ɴᴏᴡ ʜᴏsᴛᴇᴅ ᴀɴᴅ ʀᴜɴɴɪɴɢ! 🚀\n"
            f"» ᴘʀᴏᴄᴇss ɪᴅ: {process.pid}\n"
            f"» ᴛᴏ sᴛᴏᴘ ɪᴛ, ᴜsᴇ .stopclone (ɪғ ʏᴏᴜ ᴀʀᴇ ᴛʜᴇ ᴏᴡɴᴇʀ ᴏғ ᴛʜᴀᴛ ʙᴏᴛ).\n"
            f"» ᴅᴏɴ'ᴛ ғᴏʀɢᴇᴛ ᴛᴏ sᴇᴛ ᴘʀɪᴠᴀᴄʏ ᴍᴏᴅᴇ ᴏғғ ᴠɪᴀ @BotFather."
        )
        await update.effective_message.reply_text(success_text)
    except Exception as e:
        logger.error(f"Clone error: {e}", exc_info=True)
        await update.effective_message.reply_text("» ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ.")

async def handle_clone_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        if user_id not in clone_sessions or not clone_sessions[user_id]:
            return
        token = update.effective_message.text.strip()
        await update.effective_message.reply_text("» ᴡᴀɪᴛ ᴅᴇᴠᴇʟᴏᴘɪɴɢ ʏᴏᴜʀ ʙᴏᴛ...")
        await perform_clone(update, context, token, user_id, is_owner=False)
        clone_sessions[user_id] = False
        del clone_sessions[user_id]
    except Exception as e:
        logger.error(f"Error handling clone token: {e}", exc_info=True)

async def stop_clone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        if user_id not in cloned_processes:
            await update.effective_message.reply_text("» ɴᴏ ᴄʟᴏɴᴇᴅ ʙᴏᴛ ɪs ʀᴜɴɴɪɴɢ ғᴏʀ ʏᴏᴜ.")
            return

        if stop_cloned_bot(user_id):
            cloned_users = load_cloned_bots()
            if user_id in cloned_users:
                cloned_users.remove(user_id)
                save_cloned_bots(cloned_users)
            await update.effective_message.reply_text(
                f"» ᴄʟᴏɴᴇᴅ ʙᴏᴛ sᴛᴏᴘᴘᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅\n"
                f"» ʏᴏᴜ ᴄᴀɴ ʀᴇsᴛᴀʀᴛ ɪᴛ ʙʏ ʀᴜɴɴɪɴɢ ᴛʜᴇ sᴄʀɪᴘᴛ ᴀɢᴀɪɴ ᴏʀ ᴄʟᴏɴɪɴɢ ᴀɢᴀɪɴ."
            )
        else:
            await update.effective_message.reply_text("» ᴇʀʀᴏʀ sᴛᴏᴘᴘɪɴɢ ᴛʜᴇ ᴄʟᴏɴᴇᴅ ʙᴏᴛ.")
    except Exception as e:
        logger.error(f"Error in stop_clone: {e}", exc_info=True)

async def cancel_clone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        if user_id in clone_sessions:
            clone_sessions[user_id] = False
            del clone_sessions[user_id]
            await update.effective_message.reply_text("» ᴄʟᴏɴᴇ ᴘʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ ❌")
        else:
            await update.effective_message.reply_text("» ɴᴏ ᴀᴄᴛɪᴠᴇ ᴄʟᴏɴᴇ ᴘʀᴏᴄᴇss.")
    except Exception as e:
        logger.error(f"Error in cancel_clone: {e}", exc_info=True)

async def leave_command(update: Update, context: ContextTypes.DEFAULT_TYPE, args: list[str]):
    try:
        chat = update.effective_chat
        message = update.effective_message

        if chat.type == "private":
            if not args:
                await message.reply_text(
                    f"» ᴜsᴀɢᴇ: .leave <ᴄʜᴀᴛ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ>\n"
                    f"» ᴇxᴀᴍᴘʟᴇ: .leave -1001234567890  ᴏʀ  .leave @channelusername"
                )
                return
            target = args[0]
            if target.startswith("@"):
                try:
                    chat_obj = await context.bot.get_chat(target)
                    chat_id = chat_obj.id
                except Exception as e:
                    await message.reply_text(f"» ᴇʀʀᴏʀ: ᴄᴏᴜʟᴅ ɴᴏᴛ ғɪɴᴅ ᴄʜᴀᴛ – {e}")
                    return
            else:
                try:
                    chat_id = int(target)
                except ValueError:
                    await message.reply_text("» ᴇʀʀᴏʀ: ɪɴᴠᴀʟɪᴅ ᴄʜᴀᴛ ɪᴅ.")
                    return
            try:
                await context.bot.leave_chat(chat_id)
                await message.reply_text(f"» sᴜᴄᴄᴇssғᴜʟʟʏ ʟᴇғᴛ ᴄʜᴀᴛ ✅\n» ᴄʜᴀᴛ ɪᴅ: {chat_id}")
            except Exception as e:
                await message.reply_text(f"» ᴇʀʀᴏʀ ᴡʜɪʟᴇ ʟᴇᴀᴠɪɴɢ: {e}")
        else:
            try:
                await context.bot.leave_chat(chat.id)
                await message.reply_text(f"» sᴜᴄᴄᴇssғᴜʟʟʏ ʟᴇғᴛ ᴛʜɪs ɢʀᴏᴜᴘ ✅\n» ᴄʜᴀᴛ ɪᴅ: {chat.id}")
            except Exception as e:
                await message.reply_text(f"» ᴇʀʀᴏʀ ᴡʜɪʟᴇ ʟᴇᴀᴠɪɴɢ: {e}")
    except Exception as e:
        logger.error(f"Error in leave_command: {e}", exc_info=True)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        HELP_STRING = (
            "» ʙʟᴀᴄᴋᴏᴜᴛ ʜᴇʟᴘ ᴍᴇɴᴜ\n\n"
            "» ᴄʟɪᴄᴋ ᴏɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ғᴏʀ ʜᴇʟᴘ\n"
            "» ᴅᴇᴠᴇʟᴏᴘᴇʀ: @SLAYER_KI_MAA_PELNE_WALA"
        )
        HELP_BUTTONS = [
            [
                InlineKeyboardButton("• sᴘᴀᴍ •", callback_data="help:spam"),
                InlineKeyboardButton("• ʀᴀɪᴅ •", callback_data="help:raid"),
            ],
            [
                InlineKeyboardButton("• ᴇxᴛʀᴀ •", callback_data="help:extra"),
            ],
            [
                InlineKeyboardButton("• ᴄʜᴀɴɴᴇʟ •", url="https://t.me/WORLD_ALPHA"),
                InlineKeyboardButton("• sᴜᴘᴘᴏʀᴛ •", callback_data="menu:support"),
            ],
        ]
        await update.effective_message.reply_text(HELP_STRING, reply_markup=InlineKeyboardMarkup(HELP_BUTTONS))
    except Exception as e:
        logger.error(f"Error in help_command: {e}", exc_info=True)

async def sudo_command(update: Update, context: ContextTypes.DEFAULT_TYPE, args: list[str]):
    try:
        target_id = await get_target_user_from_args(update, context, args)
        if not target_id:
            await update.effective_message.reply_text("» ᴇʀʀᴏʀ: ᴄᴏᴜʟᴅ ɴᴏᴛ ɪᴅᴇɴᴛɪғʏ ᴛᴀʀɢᴇᴛ ᴜsᴇʀ.")
            return
        if target_id == OWNER_ID:
            await update.effective_message.reply_text("» ᴛʜᴇ ᴏᴡɴᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ sᴜᴅᴏ.")
            return
        sudo_users.add(target_id)
        save_data()
        await update.effective_message.reply_text(f"» sᴜᴅᴏ ᴀᴅᴅᴇᴅ ✅\n» ᴜsᴇʀ ɪᴅ: {target_id}")
    except Exception as e:
        logger.error(f"Error in sudo_command: {e}", exc_info=True)

async def rmsudo_command(update: Update, context: ContextTypes.DEFAULT_TYPE, args: list[str]):
    try:
        target_id = await get_target_user_from_args(update, context, args)
        if not target_id:
            await update.effective_message.reply_text("» ᴇʀʀᴏʀ: ᴄᴏᴜʟᴅ ɴᴏᴛ ɪᴅᴇɴᴛɪғʏ ᴛᴀʀɢᴇᴛ ᴜsᴇʀ.")
            return
        if target_id == OWNER_ID:
            await update.effective_message.reply_text("» ᴛʜᴇ ᴏᴡɴᴇʀ ᴄᴀɴɴᴏᴛ ʙᴇ ʀᴇᴍᴏᴠᴇᴅ.")
            return
        if target_id not in sudo_users:
            await update.effective_message.reply_text("» ᴛʜɪs ᴜsᴇʀ ɪs ɴᴏᴛ ɪɴ ᴛʜᴇ sᴜᴅᴏ ʟɪsᴛ.")
            return
        sudo_users.remove(target_id)
        save_data()
        await update.effective_message.reply_text(f"» sᴜᴅᴏ ʀᴇᴍᴏᴠᴇᴅ ❌\n» ᴜsᴇʀ ɪᴅ: {target_id}")
    except Exception as e:
        logger.error(f"Error in rmsudo_command: {e}", exc_info=True)

async def echo_command(update: Update, context: ContextTypes.DEFAULT_TYPE, args: list[str]):
    try:
        chat_id = update.effective_chat.id
        target_id = await get_target_user_from_args(update, context, args)
        if not target_id:
            await update.effective_message.reply_text(
                "» ᴇʀʀᴏʀ: ᴄᴏᴜʟᴅ ɴᴏᴛ ɪᴅᴇɴᴛɪғʏ ᴛᴀʀɢᴇᴛ ᴜsᴇʀ.\n"
                "» ᴜsᴀɢᴇ: .echo <ʀᴇᴘʟʏ/ᴜsᴇʀɴᴀᴍᴇ/ɪᴅ>"
            )
            return
        if target_id == OWNER_ID:
            await update.effective_message.reply_text("» ɴᴏ, ᴛʜɪs ɢᴜʏ ɪs ᴛʜᴇ ᴏᴡɴᴇʀ ᴏғ ᴛʜᴇ ʙᴏᴛ.")
            return
        if target_id in sudo_users:
            await update.effective_message.reply_text("» ɴᴏ, ᴛʜɪs ɢᴜʏ ɪs ᴀ sᴜᴅᴏ ᴜsᴇʀ.")
            return
        if chat_id not in echo_targets:
            echo_targets[chat_id] = set()
        if target_id in echo_targets[chat_id]:
            await update.effective_message.reply_text("» ᴇᴄʜᴏ ɪs ᴀʟʀᴇᴀᴅʏ ᴀᴄᴛɪᴠᴀᴛᴇᴅ ᴏɴ ᴛʜɪs ᴜsᴇʀ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.")
            return
        echo_targets[chat_id].add(target_id)
        save_data()
        await update.effective_message.reply_text(
            f"» ᴇᴄʜᴏ ᴀᴄᴛɪᴠᴀᴛᴇᴅ ᴏɴ ᴛʜᴇ ᴜsᴇʀ ✅\n"
            f"» ᴛᴀʀɢᴇᴛ ɪᴅ: {target_id}\n"
            f"» ᴛʜᴇ ʙᴏᴛ ᴡɪʟʟ ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴇɪʀ ᴍᴇssᴀɢᴇs ᴡɪᴛʜ ᴛʜᴇ sᴀᴍᴇ ᴛᴇxᴛ."
        )
    except Exception as e:
        logger.error(f"Error in echo_command: {e}", exc_info=True)

async def rmecho_command(update: Update, context: ContextTypes.DEFAULT_TYPE, args: list[str]):
    try:
        chat_id = update.effective_chat.id
        target_id = await get_target_user_from_args(update, context, args)
        if not target_id:
            await update.effective_message.reply_text(
                "» ᴇʀʀᴏʀ: ᴄᴏᴜʟᴅ ɴᴏᴛ ɪᴅᴇɴᴛɪғʏ ᴛᴀʀɢᴇᴛ ᴜsᴇʀ.\n"
                "» ᴜsᴀɢᴇ: .rmecho <ʀᴇᴘʟʏ/ᴜsᴇʀɴᴀᴍᴇ/ɪᴅ>"
            )
            return
        if chat_id not in echo_targets or target_id not in echo_targets[chat_id]:
            await update.effective_message.reply_text("» ᴇᴄʜᴏ ɪs ɴᴏᴛ ᴀᴄᴛɪᴠᴇ ᴏɴ ᴛʜɪs ᴜsᴇʀ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.")
            return
        echo_targets[chat_id].remove(target_id)
        if not echo_targets[chat_id]:
            del echo_targets[chat_id]
        save_data()
        await update.effective_message.reply_text(
            f"» ᴇᴄʜᴏ ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ ғᴏʀ ᴛʜᴇ ᴜsᴇʀ ❌\n"
            f"» ᴛᴀʀɢᴇᴛ ɪᴅ: {target_id}"
        )
    except Exception as e:
        logger.error(f"Error in rmecho_command: {e}", exc_info=True)

async def spam_command(update: Update, context: ContextTypes.DEFAULT_TYPE, args: list[str]):
    try:
        chat_id = update.effective_chat.id
        if is_protected(chat_id):
            await update.effective_message.reply_text("» ꜱᴏʀʀʏ, ᴛʜɪꜱ ɪꜱ ᴀ ᴘʀᴏᴛᴇᴄᴛᴇᴅ ɢʀᴏᴜᴘ.")
            return

        if chat_id in active_spams:
            active_spams[chat_id].cancel()
            del active_spams[chat_id]

        reply_msg = update.effective_message.reply_to_message
        if not args:
            await update.effective_message.reply_text(
                f"» ᴜsᴀɢᴇ: .spam <ᴄᴏᴜɴᴛ> [ᴛᴇxᴛ]\n"
                f"» ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴡɪᴛʜ: .spam <ᴄᴏᴜɴᴛ>"
            )
            return

        try:
            count = int(args[0])
            if count <= 0:
                raise ValueError
        except ValueError:
            await update.effective_message.reply_text("» ᴇʀʀᴏʀ: ᴄᴏᴜɴᴛ ᴍᴜsᴛ ʙᴇ ᴀ ᴘᴏsɪᴛɪᴠᴇ ɪɴᴛᴇɢᴇʀ.")
            return

        if reply_msg:
            if reply_msg.photo or reply_msg.animation or reply_msg.video or reply_msg.document:
                file_id = None
                if reply_msg.photo:
                    file_id = reply_msg.photo[-1].file_id
                elif reply_msg.animation:
                    file_id = reply_msg.animation.file_id
                elif reply_msg.video:
                    file_id = reply_msg.video.file_id
                elif reply_msg.document:
                    file_id = reply_msg.document.file_id
                caption = reply_msg.caption or ""
                task = asyncio.create_task(media_spam_task(chat_id, file_id, caption, count, context.bot))
                active_spams[chat_id] = task
                await update.effective_message.reply_text(f"» sᴘᴀᴍ sᴛᴀʀᴛᴇᴅ (ᴍᴇᴅɪᴀ) ✅\n» ᴄᴏᴜɴᴛ: {count}")
                return
            else:
                text = reply_msg.text or "Spam"
                task = asyncio.create_task(spam_task(chat_id, text, count, context.bot, reply_msg.message_id))
                active_spams[chat_id] = task
                await update.effective_message.reply_text(f"» sᴘᴀᴍ sᴛᴀʀᴛᴇᴅ (ʀᴇᴘʟʏ) ✅\n» ᴄᴏᴜɴᴛ: {count}")
                return

        if len(args) < 2:
            await update.effective_message.reply_text(
                f"» ᴜsᴀɢᴇ: .spam <ᴄᴏᴜɴᴛ> [ᴛᴇxᴛ]\n"
                f"» ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ."
            )
            return

        text = " ".join(args[1:])
        task = asyncio.create_task(spam_task(chat_id, text, count, context.bot))
        active_spams[chat_id] = task
        await update.effective_message.reply_text(f"» sᴘᴀᴍ sᴛᴀʀᴛᴇᴅ ✅\n» ᴄᴏᴜɴᴛ: {count}")
    except Exception as e:
        logger.error(f"Error in spam_command: {e}", exc_info=True)

async def pspam_command(update: Update, context: ContextTypes.DEFAULT_TYPE, args: list[str]):
    try:
        chat_id = update.effective_chat.id
        if is_protected(chat_id):
            await update.effective_message.reply_text("» ꜱᴏʀʀʏ, ᴛʜɪꜱ ɪꜱ ᴀ ᴘʀᴏᴛᴇᴄᴛᴇᴅ ɢʀᴏᴜᴘ.")
            return

        if not PSPAM_MESSAGES:
            await update.effective_message.reply_text("» ᴘsᴘᴀᴍ ᴠɪᴅᴇᴏs ᴀʀᴇ ɴᴏᴛ ᴄᴏɴғɪɢᴜʀᴇᴅ. Please add URLs to PSPAM_MESSAGES.")
            return

        try:
            count = int(args[0]) if args else 0
            if count <= 0:
                raise ValueError
        except (IndexError, ValueError):
            await update.effective_message.reply_text(f"» ᴜsᴀɢᴇ: .pspam <ᴄᴏᴜɴᴛ>")
            return

        if chat_id in active_spams:
            active_spams[chat_id].cancel()
            del active_spams[chat_id]

        task = asyncio.create_task(pspam_task(chat_id, count, context.bot))
        active_spams[chat_id] = task
        await update.effective_message.reply_text(f"» ᴘsᴘᴀᴍ sᴛᴀʀᴛᴇᴅ 🔞\n» ᴄᴏᴜɴᴛ: {count}")
    except Exception as e:
        logger.error(f"Error in pspam_command: {e}", exc_info=True)

async def raid_command(update: Update, context: ContextTypes.DEFAULT_TYPE, args: list[str], message_list):
    try:
        chat_id = update.effective_chat.id
        if is_protected(chat_id):
            await update.effective_message.reply_text("» ꜱᴏʀʀʏ, ᴛʜɪꜱ ɪꜱ ᴀ ᴘʀᴏᴛᴇᴄᴛᴇᴅ ɢʀᴏᴜᴘ.")
            return

        if not args:
            await update.effective_message.reply_text("» ᴜsᴀɢᴇ: .raid <ᴄᴏᴜɴᴛ> <ᴛᴀʀɢᴇᴛ>\nᴇxᴀᴍᴘʟᴇ: .raid 10 @ᴜsᴇʀɴᴀᴍᴇ")
            return

        try:
            count = int(args[0])
            if count <= 0:
                raise ValueError
        except ValueError:
            await update.effective_message.reply_text("» ᴇʀʀᴏʀ: ᴄᴏᴜɴᴛ ᴍᴜsᴛ ʙᴇ ᴀ ᴘᴏsɪᴛɪᴠᴇ ɪɴᴛᴇɢᴇʀ.")
            return

        target_id = await get_target_user_from_args(update, context, args[1:])
        if not target_id:
            await update.effective_message.reply_text("» ᴇʀʀᴏʀ: ᴄᴏᴜʟᴅ ɴᴏᴛ ɪᴅᴇɴᴛɪғʏ ᴛᴀʀɢᴇᴛ.")
            return

        # Protection for CRAID against sudo/owner
        if message_list is CRAID_MESSAGES:
            if target_id in sudo_users or target_id == OWNER_ID:
                if target_id == OWNER_ID:
                    await update.effective_message.reply_text("» ɴᴏ, ᴛʜɪs ɢᴜʏ ɪs ᴛʜᴇ ᴏᴡɴᴇʀ.")
                else:
                    await update.effective_message.reply_text("» ɴᴏ, ᴛʜɪs ɢᴜʏ ɪs ᴀ sᴜᴅᴏ ᴜsᴇʀ.")
                return

        if chat_id in active_raids:
            active_raids[chat_id].cancel()
            del active_raids[chat_id]

        task = asyncio.create_task(raid_task(chat_id, target_id, count, context.bot, message_list))
        active_raids[chat_id] = task
        await update.effective_message.reply_text(f"» ʀᴀɪᴅ sᴛᴀʀᴛᴇᴅ ✅\n» ᴄᴏᴜɴᴛ: {count}\n» ᴛᴀʀɢᴇᴛ ɪᴅ: {target_id}")
    except Exception as e:
        logger.error(f"Error in raid_command: {e}", exc_info=True)

async def replyraid_command(update: Update, context: ContextTypes.DEFAULT_TYPE, args: list[str]):
    try:
        chat_id = update.effective_chat.id
        target_id = await get_target_user_from_args(update, context, args)
        if not target_id:
            await update.effective_message.reply_text("» ᴇʀʀᴏʀ: ᴄᴏᴜʟᴅ ɴᴏᴛ ɪᴅᴇɴᴛɪғʏ ᴛᴀʀɢᴇᴛ.")
            return
        if target_id == OWNER_ID or target_id in sudo_users:
            await update.effective_message.reply_text("» ɴᴏ, ᴛʜɪs ɢᴜʏ ɪs ᴘʀᴏᴛᴇᴄᴛᴇᴅ.")
            return
        replyraid_targets[chat_id] = target_id
        save_data()
        await update.effective_message.reply_text(f"» ʀᴇᴩʟʏʀᴀɪᴅ ᴀᴄᴛɪᴠᴀᴛᴇᴅ ✅\n» ᴛᴀʀɢᴇᴛ ɪᴅ: {target_id}")
    except Exception as e:
        logger.error(f"Error in replyraid_command: {e}", exc_info=True)

async def stop_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_id = update.effective_chat.id
        if chat_id in active_spams:
            active_spams[chat_id].cancel()
            del active_spams[chat_id]
            await update.effective_message.reply_text("» sᴘᴀᴍ ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ ❌")
        else:
            await update.effective_message.reply_text("» ɴᴏ ᴀᴄᴛɪᴠᴇ sᴘᴀᴍ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.")
    except Exception as e:
        logger.error(f"Error in stop_spam: {e}", exc_info=True)

async def stop_raid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_id = update.effective_chat.id
        if chat_id in active_raids:
            active_raids[chat_id].cancel()
            del active_raids[chat_id]
            await update.effective_message.reply_text("» ʀᴀɪᴅ ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ ❌")
        else:
            await update.effective_message.reply_text("» ɴᴏ ᴀᴄᴛɪᴠᴇ ʀᴀɪᴅ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.")
    except Exception as e:
        logger.error(f"Error in stop_raid: {e}", exc_info=True)

async def stop_replyraid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_id = update.effective_chat.id
        if chat_id in replyraid_targets:
            del replyraid_targets[chat_id]
            save_data()
            await update.effective_message.reply_text("» ʀᴇᴩʟʏʀᴀɪᴅ ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ ❌")
        else:
            await update.effective_message.reply_text("» ɴᴏ ᴀᴄᴛɪᴠᴇ ʀᴇᴘʟʏʀᴀɪᴅ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.")
    except Exception as e:
        logger.error(f"Error in stop_replyraid: {e}", exc_info=True)

async def ultimate_spam(update: Update, context: ContextTypes.DEFAULT_TYPE, args: list[str]):
    try:
        chat_id = update.effective_chat.id
        if is_protected(chat_id):
            await update.effective_message.reply_text("» ꜱᴏʀʀʏ, ᴛʜɪꜱ ɪꜱ ᴀ ᴘʀᴏᴛᴇᴄᴛᴇᴅ ɢʀᴏᴜᴘ.")
            return

        reply_msg = update.effective_message.reply_to_message
        if not args and not reply_msg:
            await update.effective_message.reply_text(
                "» ᴜsᴀɢᴇ: .uspam <ᴛᴀʀɢᴇᴛ> <ᴛᴇxᴛ>\n"
                "» ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴀɴᴅ ᴜsᴇ .uspam <ᴛᴇxᴛ>"
            )
            return

        await stop_ultimate_type(update, context, "spam", silent=True)

        target_id = None
        mention = None
        text = None

        if reply_msg:
            target_id = reply_msg.from_user.id
            target_user = reply_msg.from_user
            mention = get_user_mention(target_user)
            if args:
                text = " ".join(args)
            else:
                text = reply_msg.text or "Spam"
        else:
            if args:
                potential_target = args[0]
                if potential_target.startswith("@"):
                    try:
                        chat = await context.bot.get_chat(potential_target)
                        target_id = chat.id
                        target_user = chat
                        mention = get_user_mention(target_user)
                        text = " ".join(args[1:]) if len(args) > 1 else "Spam"
                    except Exception:
                        target_id = None
                        mention = None
                        text = " ".join(args)
                elif potential_target.isdigit():
                    try:
                        target_id = int(potential_target)
                        target_user = await context.bot.get_chat(target_id)
                        mention = get_user_mention(target_user)
                        text = " ".join(args[1:]) if len(args) > 1 else "Spam"
                    except Exception:
                        target_id = None
                        mention = None
                        text = " ".join(args)
                else:
                    target_id = None
                    mention = None
                    text = " ".join(args)
            else:
                return

        if not text:
            text = "Spam"

        task = asyncio.create_task(ultimate_spam_task(chat_id, mention, text, context.bot, reply_msg.message_id if reply_msg else None))
        if chat_id not in ultimate_tasks:
            ultimate_tasks[chat_id] = {}
        ultimate_tasks[chat_id]["spam"] = task

        await update.effective_message.reply_text(
            "» ᴜʟᴛɪᴍᴀᴛᴇ sᴘᴀᴍ sᴛᴀʀᴛᴇᴅ ✅\n"
            "» ᴛᴏ sᴛᴏᴘ, ᴜsᴇ .sᴛᴏᴘᴜsᴘᴀᴍ"
        )
    except Exception as e:
        logger.error(f"Error in ultimate_spam: {e}", exc_info=True)

async def ultimate_raid(update: Update, context: ContextTypes.DEFAULT_TYPE, args: list[str], message_list, raid_type: str):
    try:
        chat_id = update.effective_chat.id
        if is_protected(chat_id):
            await update.effective_message.reply_text("» ꜱᴏʀʀʏ, ᴛʜɪꜱ ɪꜱ ᴀ ᴘʀᴏᴛᴇᴄᴛᴇᴅ ɢʀᴏᴜᴘ.")
            return

        if not args:
            cmd_name = update.effective_message.text.split()[0]
            await update.effective_message.reply_text(
                f"» ᴜsᴀɢᴇ: .{cmd_name} <ᴛᴀʀɢᴇᴛ>\n"
                f"» ᴇxᴀᴍᴘʟᴇ: .{cmd_name} @ᴜsᴇʀɴᴀᴍᴇ"
            )
            return

        target_id = await get_target_user_from_args(update, context, args)
        if not target_id:
            await update.effective_message.reply_text("» ᴇʀʀᴏʀ: ᴄᴏᴜʟᴅ ɴᴏᴛ ɪᴅᴇɴᴛɪғʏ ᴛᴀʀɢᴇᴛ.")
            return

        if not message_list:
            await update.effective_message.reply_text("» ᴇʀʀᴏʀ: ᴛʜᴇ ᴍᴇssᴀɢᴇ ʟɪsᴛ ғᴏʀ ᴛʜɪs ʀᴀɪᴅ ᴛʏᴘᴇ ɪs ᴇᴍᴘᴛʏ.")
            return

        if raid_type == "alphabet" and (target_id in sudo_users or target_id == OWNER_ID):
            if target_id == OWNER_ID:
                await update.effective_message.reply_text("» ɴᴏ, ᴛʜɪs ɢᴜʏ ɪs ᴛʜᴇ ᴏᴡɴᴇʀ.")
            else:
                await update.effective_message.reply_text("» ɴᴏ, ᴛʜɪs ɢᴜʏ ɪs ᴀ sᴜᴅᴏ ᴜsᴇʀ.")
            return

        await stop_ultimate_type(update, context, raid_type, silent=True)

        task = asyncio.create_task(ultimate_raid_task(chat_id, target_id, context.bot, message_list))
        if chat_id not in ultimate_tasks:
            ultimate_tasks[chat_id] = {}
        ultimate_tasks[chat_id][raid_type] = task

        type_names = {
            "general": "ɢᴇɴᴇʀᴀʟ",
            "love": "ʟᴏᴠᴇ",
            "shayari": "sʜᴀʏᴀʀɪ",
            "alphabet": "ᴀʟᴘʜᴀʙᴇᴛ"
        }
        type_display = type_names.get(raid_type, raid_type)

        stop_cmd = {
            "general": ".sᴛᴏᴘᴜʀᴀɪᴅ",
            "love": ".sᴛᴏᴘᴜᴍʀᴀɪᴅ",
            "shayari": ".sᴛᴏᴘᴜsʀᴀɪᴅ",
            "alphabet": ".sᴛᴏᴘᴜᴄʀᴀɪᴅ"
        }.get(raid_type, ".sᴛᴏᴘᴀʟʟ")

        await update.effective_message.reply_text(
            f"» ᴜʟᴛɪᴍᴀᴛᴇ {type_display} ʀᴀɪᴅ sᴛᴀʀᴛᴇᴅ ✅\n"
            f"» ᴛᴀʀɢᴇᴛ ɪᴅ: {target_id}\n"
            f"» ᴛᴏ sᴛᴏᴘ, ᴜsᴇ {stop_cmd}"
        )
    except Exception as e:
        logger.error(f"Error in ultimate_raid: {e}", exc_info=True)

async def stop_ultimate_type(update: Update, context: ContextTypes.DEFAULT_TYPE, task_type: str, silent: bool = False):
    try:
        chat_id = update.effective_chat.id
        if chat_id not in ultimate_tasks or task_type not in ultimate_tasks[chat_id]:
            if not silent:
                await update.effective_message.reply_text(f"» ɴᴏ ᴀᴄᴛɪᴠᴇ ᴜʟᴛɪᴍᴀᴛᴇ {task_type} ᴛᴀsᴋ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.")
            return

        task = ultimate_tasks[chat_id][task_type]
        if not task.done():
            task.cancel()
        del ultimate_tasks[chat_id][task_type]
        if not ultimate_tasks[chat_id]:
            del ultimate_tasks[chat_id]

        if not silent:
            type_names = {
                "spam": "sᴘᴀᴍ",
                "general": "ɢᴇɴᴇʀᴀʟ ʀᴀɪᴅ",
                "love": "ʟᴏᴠᴇ ʀᴀɪᴅ",
                "shayari": "sʜᴀʏᴀʀɪ ʀᴀɪᴅ",
                "alphabet": "ᴀʟᴘʜᴀʙᴇᴛ ʀᴀɪᴅ"
            }
            display = type_names.get(task_type, task_type)
            await update.effective_message.reply_text(f"» ᴜʟᴛɪᴍᴀᴛᴇ {display} sᴛᴏᴘᴘᴇᴅ ❌")
    except Exception as e:
        logger.error(f"Error in stop_ultimate_type: {e}", exc_info=True)

async def stop_all_ultimate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_id = update.effective_chat.id
        if chat_id not in ultimate_tasks or not ultimate_tasks[chat_id]:
            await update.effective_message.reply_text("» ɴᴏ ᴀᴄᴛɪᴠᴇ ᴜʟᴛɪᴍᴀᴛᴇ ᴛᴀsᴋs ɪɴ ᴛʜɪs ᴄʜᴀᴛ.")
            return

        cancelled = 0
        for task in ultimate_tasks[chat_id].values():
            if not task.done():
                task.cancel()
                cancelled += 1
        ultimate_tasks[chat_id].clear()
        del ultimate_tasks[chat_id]

        await update.effective_message.reply_text(
            f"» ᴀʟʟ ᴜʟᴛɪᴍᴀᴛᴇ ᴛᴀsᴋs sᴛᴏᴘᴘᴇᴅ ❌\n"
            f"» ᴄᴀɴᴄᴇʟʟᴇᴅ {cancelled} ᴛᴀsᴋs."
        )
    except Exception as e:
        logger.error(f"Error in stop_all_ultimate: {e}", exc_info=True)

async def name_change(update: Update, context: ContextTypes.DEFAULT_TYPE, args: list[str]):
    try:
        chat_id = update.effective_chat.id
        if not args:
            await update.effective_message.reply_text("» ᴜsᴀɢᴇ: .nc <ᴛᴇxᴛ>")
            return

        base_text = " ".join(args)
        if chat_id in name_change_tasks:
            name_change_tasks[chat_id].cancel()
            del name_change_tasks[chat_id]

        task = asyncio.create_task(name_change_task(chat_id, base_text, context.bot))
        name_change_tasks[chat_id] = task
        await update.effective_message.reply_text(
            "» ɴᴀᴍᴇ ᴄʜᴀɴɢɪɴɢ sᴛᴀʀᴛᴇᴅ ✅ (sᴍᴀʀᴛ ғʟᴏᴏᴅ-ʟᴇss ᴍᴏᴅᴇ)\n"
            "» ᴛᴏ sᴛᴏᴘ, ᴜsᴇ .sᴛᴏᴘɴᴄ"
        )
    except Exception as e:
        logger.error(f"Error in name_change: {e}", exc_info=True)

async def stop_name_change(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_id = update.effective_chat.id
        if chat_id in name_change_tasks and not name_change_tasks[chat_id].done():
            name_change_tasks[chat_id].cancel()
            del name_change_tasks[chat_id]
            await update.effective_message.reply_text("» ɴᴀᴍᴇ ᴄʜᴀɴɢɪɴɢ sᴛᴏᴘᴘᴇᴅ ❌")
        else:
            await update.effective_message.reply_text("» ɴᴏ ᴀᴄᴛɪᴠᴇ ɴᴀᴍᴇ ᴄʜᴀɴɢᴇ ᴛᴀsᴋ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.")
    except Exception as e:
        logger.error(f"Error in stop_name_change: {e}", exc_info=True)

# ==================== MESSAGE HANDLER (replyraid & echo) ====================
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        if user_id in clone_sessions and clone_sessions[user_id]:
            await handle_clone_token(update, context)
            return

        chat_id = update.effective_chat.id
        message = update.effective_message
        if not message or not message.from_user or message.from_user.is_bot:
            return

        # ReplyRaid
        if chat_id in replyraid_targets and message.from_user.id == replyraid_targets[chat_id]:
            if REPLYRAID_MESSAGES:
                random_text = random.choice(REPLYRAID_MESSAGES)
                mention = get_user_mention(message.from_user)
                reply_text = f"{mention} {random_text}"
                try:
                    await message.reply_text(reply_text, parse_mode=constants.ParseMode.MARKDOWN)
                except Exception:
                    pass

        # Echo
        if chat_id in echo_targets and message.from_user.id in echo_targets[chat_id] and message.text:
            try:
                await message.reply_text(message.text)
            except Exception:
                pass
    except Exception as e:
        logger.error(f"Error in message_handler: {e}", exc_info=True)

# ==================== MAIN ====================
def main():
    load_data()

    # Restore cloned bots (safe)
    cloned_users = load_cloned_bots()
    for uid in list(cloned_users):
        try:
            if uid not in cloned_processes:
                process = start_cloned_bot(uid)
                if process:
                    cloned_processes[uid] = process
                else:
                    cloned_users.discard(uid)
                    save_cloned_bots(cloned_users)
        except Exception:
            continue

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cancel", cancel_clone))
    app.add_handler(CommandHandler("stopclone", stop_clone))

    app.add_handler(
        MessageHandler(filters.TEXT & filters.Regex(r'^\.'), handle_dot_commands)
    )
    app.add_handler(
        MessageHandler(filters.ALL & ~filters.COMMAND, message_handler)
    )
    app.add_handler(CallbackQueryHandler(button_callback))

    print("BOT IS WORKING (crash‑proof edition)")
    try:
        app.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.critical(f"Fatal error in main loop: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()