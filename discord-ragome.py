from selenium.webdriver.chrome.options import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
import asyncio
import nest_asyncio
import time
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
from selenium.webdriver.common.by import By
# Chrome driver 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager
import os

# Chrome driver Manager를 통해 크롬 드라이버 자동 설치 > 최신 버전을 설치 > Service에 저장
service = Service(excutable_path=ChromeDriverManager().install()) 
# 파일 r 모드로 열기
TOKEN = os.environ["BOT_TOKEN"]
nest_asyncio.apply()




@bot.event
async def on_message(message): 
    if message.content.startswith ("/인증 "):
        message_content = message.content.replace("/인증 ", "")
        url = message_content.replace(" ", "")

        if 'chzzk.naver.com/' not in url:
            await message.delete()
            embed = discord.Embed(title="주소 오류", description=message.author.mention + '님', color = 0xff0000)
            embed.add_field(name = '', value="현재 주소가 잘 못 되어있습니다.", inline=True)
            embed.add_field(name = '', value="치지직 주소가 맞는지 다시 확인 바랍니다.", inline=False)
            sleep_m = await message.channel.send (embed=embed)

        else:
            if 'https://m.chzzk.naver.com/' in url:
                url = message_content.replace("https://m.chzzk.naver.com/", "https://chzzk.naver.com/")
            if '.naver.com/live/' in url:
                url = url.replace("live/", "")
            
            await message.delete()
            embed = discord.Embed(title="치지직 확인 중", description=message.author.mention + '님', color = discord.Color.yellow())
            embed.add_field(name = '', value="잠시 기다려 주세요...", inline=True)
            sleep_m = await message.channel.send (embed=embed)
            
            
            
            options = Options()
            options.add_argument("headless")
            driver = webdriver.Chrome(service=service, options=options)
            driver.get(url)
            time.sleep(1)
            
            # 이름, 팔로우 수, 프사 반환
            c_name = driver.find_element(By.XPATH,'//*[@id="layout-body"]/div/section/div[1]/div/div/div[1]/h2/span/span')
            Follow = driver.find_element(By.XPATH,'//*[@id="layout-body"]/div/section/div[1]/div/div/div[1]/div/span')
            img = driver.find_element(By.XPATH,'//*[@id="layout-body"]/div/section/div[1]/a/img').get_attribute("src")
            
            
            # 이름
            c_name = c_name.text
            
            
            
            #팔로우
            Follow = Follow.text.split('팔로워 ')[1]
            if Follow.find('천') > -1:
                Follow = int(float(Follow.split('천')[0])*1000)
            elif Follow.find('만')  > -1:
                Follow = int(float(Follow.split('만')[0])*10000)
            else:
                Follow = int(Follow.split('명')[0])
            
            
            
            # 다시보기 수
            time.sleep(1)
            driver.get(f'{url}/videos?videoType=&sortType=LATEST&page=1')
            time.sleep(1)
            try: # 다시보기 있음
                live_list = driver.find_element(By.XPATH,'//*[@id="videos-PANEL"]/ul')
                live_list = len(live_list.text.split('다시보기')) -1
            except: # 다시보기 있음
                live_list = 0
            
            
            
            # 총 라이브 시간 가져오기 
            time.sleep(1)
            driver.get(f'{url}/about')
            time.sleep(1)
    
            try:    
                live_time = driver.find_element(By.XPATH,'//*[@id="about-PANEL"]/div/div[2]/span[2]')
                live_time = int(live_time.text.split(' 시간')[0].replace(',',''))
            
            except:
                try:                                                      
                    live_time = driver.find_element(By.XPATH,'//*[@id="about-PANEL"]/div[2]/div[2]/span[2]')
                    live_time = int(live_time.text.split(' 시간')[0].replace(',',''))
    
                except:
                    live_time = driver.find_element(By.XPATH,'//*[@id="about-PANEL"]/div[3]/div[2]/span[2]')
                    live_time = int(live_time.text.split(' 시간')[0].replace(',',''))
            
            
            time.sleep(1)
            driver.quit()
            
            
            ########################################################################################
            
            
            # 인증 가능 조건
            F = Follow >= 200
            l_t = live_time >= 500
            l_l = live_list >= 6
            T_F_lsit = [F, l_t, l_l]
            
            
            
            if T_F_lsit.count(True) >= 2:
                await sleep_m.delete()
                await message.author.edit(nick=c_name)
                time.sleep(1)
                embed = discord.Embed(title="인증 시스템", description=message.author.mention + '님', color= 0xff00)
                embed.add_field(name = '', value="인증이 정상적으로 완료 되었습니다 !", inline=True)
                embed.set_thumbnail(url=img)
                await message.channel.send (embed=embed)
                role_id = 1309211371434410065 # 기본 권한 ID
                role = discord.utils.get(message.guild.roles, id = role_id)
                await message.author.add_roles(role)
                
            else:
                await sleep_m.delete()
                await message.author.edit(nick=c_name)
                time.sleep(1)
                await message.channel.send(embed=discord.Embed(title="조건 부족", description = message.author.mention + "님은 조건에 부합되지 않습니다.", color = 0xff0000))


bot.run(TOKEN)
