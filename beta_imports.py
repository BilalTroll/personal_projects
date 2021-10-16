from pycoingecko import CoinGeckoAPI
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from parameters import *

import requests
import discord
import os 
import time
import ctypes 

#DISCORD STUFF/EDITABLES
client = discord.Client()
os.system("cls")
channel = client.get_channel(int(channel_ID))

#CHROME STUFF
chrome_options = Options()
user32 = ctypes.windll.user32

length = user32.GetSystemMetrics(0)
width = user32.GetSystemMetrics(1)

PATH = "C:\Program Files (x86)\chromedriver.exe"

if debugMode == False:
                chrome_options.add_argument("--headless")
        
driver = webdriver.Chrome(PATH,options=chrome_options)
driver.set_window_size(length,width)           


def energiopener(link):
        driver.get(link)
        timeout = 5
        try:
                WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="center"]/div/div/div/div[4]/div/div[3]/div[1]/div[1]/div[5]')))
        except TimeoutException:
                print("Waiting for page to load.")
        finally:
                print("Page loaded")


