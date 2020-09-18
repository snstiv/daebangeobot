import discord
import asyncio
import random
import openpyxl
from discord import Member
from discord.ext import commands
import youtube_dl
from urllib.request import urlopen, Request
import emoji
from discord.ext.commands import bot
from discord.utils import get
import urllib
import urllib.request
import bs4
import os
import sys
import json
from selenium import webdriver
import time
import datetime


from selenium.webdriver.support import color

client = discord.Client()

# 복사해 둔 토큰을 your_token에 넣어줍니당
token = "your_token"
searchYoutubeHref={}
players = {}
queues= {}
musiclist=[]
defmafia=False
ant: int = 0
searchYoutube={}
ismbtrue = False  # 대방어마블 시작스위치
mbplayer = {}  # 대방어마블 플레이어 목록
count = 0
bot = commands.Bot(command_prefix='!')

# 봇이 구동되었을 때 동작되는 코드
@client.event
async def on_ready():
    defmafia = False
    print("로그인 된 봇:")  # 화면에 봇의 아이디, 닉네임이 출력되는 코드
    print(client.user.name)
    print(client.user.id)
    print("===========")

def check_queue(id):

    if queues[id]!=[]:
        player = queues[id].pop(0)
        players[id] = player
        del musiclist[0]
        player.start()


@client.event
async def on_ready():
    global GAME
    GAME = "마블종료"
    await client.change_presence(status=discord.Status.offline)
    game = discord.Game("시작하는 중...")
    await client.change_presence(status=discord.Status.online, activity=game)
    while True:
        game = discord.Game("작전 계획")
        await client.change_presence(status=discord.Status.online, activity=game)

global LIST_COUNT


@client.event
async def on_message(message):
    global LIST_COUNT
    LIST_COUNT = 0
    cnt = 0
    if message.author.bot:  # 만약 메시지를 보낸사람이 봇일 경우에
        return None  # 동작하지 않고 무시함.
    id = message.author.id  # id라는 변수에는 메시지를 보낸사람의 ID를 담습니다.
    channel = message.channel  # channel이라는 변수에는 메시지를 받은 채널의 ID를 담습니다.
    if message.content.endswith('!대방어'):
        channel = message.channel
        await channel.send('안녕하세요, !대방어리스트 명령어로 제 명령어를 확인하십시오.')

    if message.content.endswith('!대방어리스트'):
        channel = message.channel
        embed = discord.Embed(
            title='대방어리스트',
            description='!대방어날씨 (지역) : 빅대방어를 통해 원하는 지역의 날씨 정보를 출력합니다.\n'
                        '!대방어결투 (상대) : (상대)에게 대방어결투를 신청합니다. \n',
            colour=discord.Colour.gold()
        )
        await channel.send(embed=embed)
    if message.content.startswith("!대방어날씨"):
        if message.author == client.user:  # 만약 메시지를 보낸 사람과 봇이 서로 같을 때
            return
        learn = message.content.split(" ")
        location = learn[1]
        enc_location = urllib.parse.quote(location+'날씨')
        hdr = {'User-Agent': 'Mozilla/5.0'}
        url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + enc_location
        await channel.send(url)
        req = Request(url, headers=hdr)
        html = urllib.request.urlopen(req)
        bsObj = bs4.BeautifulSoup(html, "html.parser")
        todayBase = bsObj.find('div', {'class': 'main_info'})

        todayTemp1 = todayBase.find('span', {'class': 'todaytemp'})
        todayTemp = todayTemp1.text.strip()  # 온도


        todayValueBase = todayBase.find('ul', {'class': 'info_list'})
        todayValue2 = todayValueBase.find('p', {'class': 'cast_txt'})
        todayValue = todayValue2.text.strip()  # 밝음,어제보다 ?도 높거나 낮음을 나타내줌


        todayFeelingTemp1 = todayValueBase.find('span', {'class': 'sensible'})
        todayFeelingTemp = todayFeelingTemp1.text.strip()  # 체감온도


        todayMiseaMongi1 = bsObj.find('div', {'class': 'sub_info'})
        todayMiseaMongi2 = todayMiseaMongi1.find('div', {'class': 'detail_box'})
        todayMiseaMongi3 = todayMiseaMongi2.find('dd')
        todayMiseaMongi = todayMiseaMongi3.text  # 미세먼지


        tomorrowBase = bsObj.find('div', {'class': 'table_info weekly _weeklyWeather'})
        tomorrowTemp1 = tomorrowBase.find('li', {'class': 'date_info'})
        tomorrowTemp2 = tomorrowTemp1.find('dl')
        tomorrowTemp3 = tomorrowTemp2.find('dd')
        tomorrowTemp = tomorrowTemp3.text.strip()  # 오늘 오전,오후온도



        embed = discord.Embed(
            title=learn[1]+ ' 날씨 정보',
            description=learn[1]+ '날씨 정보입니다.',
            colour=discord.Colour.gold()
        )
        embed.add_field(name='현재온도', value=todayTemp+'˚', inline=False)  # 현재온도
        embed.add_field(name='체감온도', value=todayFeelingTemp, inline=False)  # 체감온도
        embed.add_field(name='현재상태', value=todayValue, inline=False)  # 밝음,어제보다 ?도 높거나 낮음을 나타내줌
        embed.add_field(name='현재 미세먼지 상태', value=todayMiseaMongi, inline=False)  # 오늘 미세먼지
        embed.add_field(name='오늘 오전/오후 날씨', value=tomorrowTemp, inline=False)  # 오늘날씨 # color=discord.Color.blue()
        embed.add_field(name='**----------------------------------**',value='**----------------------------------**', inline=False)  # 구분선
        await channel.send(embed=embed)
#-------------------------------------------------------------------------------------------------#

    id = message.author.id  # id라는 변수에는 메시지를 보낸사람의 ID를 담습니다.
    channel = message.channel  # channel이라는 변수에는 메시지를 받은 채널의 ID를 담습니다.

    if message.content.startswith("!대방어결투"):
        a = random.randrange(10, 99)
        b = random.randrange(10, 99)
        c = a * b
        if message.author == client.user:  # 만약 메시지를 보낸 사람과 봇이 서로 같을 때
            return
        learn = message.content.split(" ")
        location = learn[1]
        player = message.author.id
        embed = discord.Embed(
            title=location + ', 결투를 신청한다!',
            description='네 의견은 상관없다! \n'
                        '10초 주겠다..',
            colour=discord.Colour.gold()
        )

        msg = await channel.send(embed=embed)
        fight = False
        try:
            await client.wait_for('DEFENSE_MAFIA_TIME',timeout=10.0)
        except:
            embed2 = discord.Embed(
                title='결투를 시작한다!',
                description='주어진 미션을 더 빨리, 정확히 완료한 자가 승리한다!',
                colour=discord.Colour.dark_red())
            await channel.send(embed=embed2)
            try:
                embed2 = discord.Embed(
                    title='준비하시고...',
                    colour=discord.Colour.dark_red())
                await channel.send(embed=embed2)
                await client.wait_for('DEFENSE_MAFIA_TIME', timeout=random.randrange(1, 7))
            except:

                embed2 = discord.Embed(
                    title='미션이다!',
                    description=str(a) + ' x ' + str(b) + ' 는?\n'
                                '30초 뒤 정답을 공개하겠다!\n',
                    colour=discord.Colour.dark_red())
                await channel.send(embed=embed2)
                try:
                    await client.wait_for('DEFENSE_MAFIA_TIME', timeout=30.0)

                except:
                    embed2 = discord.Embed(
                        title='시간 초과다, 이 애송이들아!',
                        description='답은 ' + str(c) + '(이)다.',
                        colour=discord.Colour.blue())
                    await channel.send(embed=embed2)




client.run("NzM4OTk4MDIzMTg2ODA4OTMz.XyUDig.oKrfNtgY3V5D4gbZu3MWMDj_Y3k")


