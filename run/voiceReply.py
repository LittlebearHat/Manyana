# -*- coding: utf-8 -*-
import asyncio
import json
import os
import datetime
import random
import re
import time
import sys

import httpx
import requests
import utils
from mirai import Image, Voice
from mirai import Mirai, WebSocketAdapter, FriendMessage, GroupMessage, At, Plain

from plugins.RandomStr import random_str
from plugins.modelsLoader import modelLoader
from plugins.translater import translate


def main(bot,app_id,app_key,logger):
    logger.info("语音合成用户端启动....")

    models,default,characters=modelLoader()#读取模型

    # modelSelect=['voiceModel/selina/selina.pth','voiceModel/selina/config.json']
    # print('------\n'+str(CHOISE))
    @bot.on(GroupMessage)
    async def botSaid(event:GroupMessage):
        msg = "".join(map(str, event.message_chain[Plain]))
        # 匹配指令
        m = re.match(r'^说\s*(.*)\s*$', msg.strip())
        if m and str(event.message_chain).split("说")[0] not in characters:
            # 取出指令中的地名
            text = m.group(1)
            path = '../data/voices/' + random_str() + '.wav'
            text = await translate(text, app_id, app_key)
            tex = '[JA]' + text + '[JA]'
            logger.info("启动文本转语音：text: " + tex + " path: " + path[3:])
            await voiceGenerate({"text": tex, "out": path})
            await bot.send(event, Voice(path=path[3:]))

    @bot.on(GroupMessage)
    async def botSaid(event: GroupMessage):
        msg = "".join(map(str, event.message_chain[Plain]))
        # 匹配指令
        m = re.match(r'^中文\s*(.*)\s*$', msg.strip())
        if m and str(event.message_chain).split("中文")[0] not in characters:
            # 取出指令中的地名
            text = m.group(1)
            path = '../data/voices/' + random_str() + '.wav'
            #text = await translate(text, app_id, app_key)
            tex = '[ZH]' + text + '[ZH]'
            logger.info("启动文本转语音：text: " + tex + " path: " + path[3:])
            await voiceGenerate({"text": tex, "out": path})
            await bot.send(event, Voice(path=path[3:]))

    @bot.on(GroupMessage)
    async def botSaid(event: GroupMessage):
        msg = "".join(map(str, event.message_chain[Plain]))
        # 匹配指令
        m = re.match(r'^日文\s*(.*)\s*$', msg.strip())
        if m and str(event.message_chain).split("日文")[0] not in characters:
            # 取出指令中的地名
            text = m.group(1)
            path = '../data/voices/' + random_str() + '.wav'
            # text = await translate(text, app_id, app_key)
            tex = '[JA]' + text + '[JA]'
            logger.info("启动文本转语音：text: " + tex + " path: " + path[3:])
            await voiceGenerate({"text": tex, "out": path})
            await bot.send(event, Voice(path=path[3:]))

    @bot.on(GroupMessage)
    async def characterSpeake(event:GroupMessage):
        if "说" in str(event.message_chain) and str(event.message_chain).split("说")[0] in characters:
            speaker=str(event.message_chain).split("说")[0]
            text = str(event.message_chain).split("说")[1]
            text =await translate(text, app_id, app_key)
            out = '../data/voices/' + random_str() + '.wav'
            logger.info("语音生成_文本" + text)
            logger.info("语音生成_模型:"+speaker + str(characters.get(speaker)[1]))
            data = {"text": "[JA]" + text + "[JA]", "out": out,'speaker':characters.get(speaker)[0],'modelSelect':characters.get(speaker)[1]}
            await voiceGenerate(data)
            await bot.send(event, Voice(path=out[3:]))

    @bot.on(GroupMessage)
    async def characterSpeake(event: GroupMessage):
        if "中文" in str(event.message_chain) and str(event.message_chain).split("中文")[0] in characters:
            speaker = str(event.message_chain).split("中文")[0]
            text = str(event.message_chain).split("中文")[1]
            #text = translate(text, app_id, app_key)不用翻译
            out = '../data/voices/' + random_str() + '.wav'
            logger.info("语音生成_文本" + text)
            logger.info("语音生成_模型:" + speaker + str(characters.get(speaker)[1]))
            data = {"text": "[ZH]" + text + "[ZH]", "out": out, 'speaker': characters.get(speaker)[0],
                    'modelSelect': characters.get(speaker)[1]}
            await voiceGenerate(data)
            await bot.send(event, Voice(path=out[3:]))

    @bot.on(GroupMessage)
    async def characterSpeake(event: GroupMessage):
        if "日文" in str(event.message_chain) and str(event.message_chain).split("日文")[0] in characters:
            speaker = str(event.message_chain).split("日文")[0]
            text = str(event.message_chain).split("日文")[1]
            # text = translate(text, app_id, app_key)不用翻译
            logger.info("语音生成_文本"+text)
            out = '../data/voices/' + random_str() + '.wav'
            logger.info("语音生成_模型:" + speaker + str(characters.get(speaker)[1]))
            data = {"text": "[JA]" + text + "[JA]", "out": out, 'speaker': characters.get(speaker)[0],
                    'modelSelect': characters.get(speaker)[1]}
            await voiceGenerate(data)
            await bot.send(event, Voice(path=out[3:]))

    async def voiceGenerate(data):
        # 向本地 API 发送 POST 请求
        url = 'http://localhost:9080/synthesize'
        data = json.dumps(data)
        async with httpx.AsyncClient(timeout=None) as client:
            await client.post(url, json=data)
        logger.info("语音生成完成")

