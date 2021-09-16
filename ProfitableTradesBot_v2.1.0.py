from pycoingecko import CoinGeckoAPI
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import requests
import discord
import os #color adding
import time
import ctypes #used for resolution capture of screen

#Connecting to server 
TOKEN = "ENTER TOKEN HERE"

#start discord
client = discord.Client()

#Turn on to see prints to console
debugMode = False

#calculates the iteration number
iteration = 0
@client.event
async def on_ready():
    while True:
        global iteration
        iteration = iteration + 1
        
        #fail-safe to make sure the amount of coingecko ID and energiswap assets are the exact same.
        esasset_counter = 0
        
        #discord channel ID
        discord_coins_to_enter = client.get_channel()

        #add's color to system
        os.system("cls")
        
        #calls coingecko api
        cg = CoinGeckoAPI()
        entire_list = cg.get_coins_list()

        #headless options
        chrome_options = Options()
        
        #if not in debug mode, run headless.
        if debugMode == False:
            chrome_options.add_argument("--headless")

        #prepares the symbol string which contains all symbols not yet in a list
        symbol_total_string = ""
        name_total_string = ""
        energiswap_price_total = ""

        #Enter this as a percentage.
        user_set_profit = 7


        #minimum liquidity allowed
        liquidity_limit = 10000

        #ping alert above certain threshold, enter it as trade %
        ping_alert = 10

        await discord_coins_to_enter.send("**Iteration number: **" + str(iteration))
        #await discord_coins_to_enter.send("**Minimum Trade difference is: **" + str(user_set_profit) +"%" + "\n**Minmum Liquidity is: **" + "$" + str(liquidity_limit) +"\n")
        time.sleep(5)
        
        #captures resolution of screen.
        user32 = ctypes.windll.user32
        length = user32.GetSystemMetrics(0)
        width = user32.GetSystemMetrics(1)

        #prepares path for driver and window size. Must take up at least half of screen.
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH,options=chrome_options)
        driver.set_window_size(length,width)

        #chrome driver opens energi-swap main site, then sleeps to fully open webpage.
        driver.get("enterlink")
        timeout = 5
        try:
            WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="center"]/div/div/div/div[4]/div/div[3]/div[1]/div[1]/div[5]')))
        except TimeoutException:
            print("Waiting for page to load.")
        finally:
            print("Page loaded")

        #creates empty lists for usage
        energiswap_liquidity_list = []
        energiswap_price_list = []
        symbol_list = []

        for energiswap_page in range(0,4): #four pages of energiswap
            try:
                for coin in range(50): #50 coins a page
                    symbol_element = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div/div[2]/div/div[3]/div['+str(coin+1)+']/div[1]/div[2]/div')
                    if len(symbol_element.get_attribute('innerHTML')) > 20: #checks to see if the output would be really long(BADGER ISSUE), if it is, go one division further.
                        symbol_element = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div/div[2]/div/div[3]/div['+str(coin+1)+']/div[1]/div[2]/div/div')
                    symbol_output = symbol_element.get_attribute('innerHTML')
                    symbol_list.append(symbol_output.lower())

                    #Scrapes name of coin
                    name_element = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div/div[2]/div/div[3]/div['+str(coin+1) +']/div[1]/div[1]/div/a/div')
                    if len(name_element.get_attribute('innerHTML')) > 20:
                        name_element = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div/div[2]/div/div[3]/div[' + str(coin+1) +']/div[1]/div[1]/div/a/div/div')
                    name_output = name_element.get_attribute('innerHTML')
                    name_total_string = name_total_string +  name_output + "\n"
                    
                    #energiswap price tracking
                    energiswap_price_element = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div/div[2]/div/div[3]/div['+ str(coin+1) +']/div[1]/div[5]')
                    energiswap_price = energiswap_price_element.get_attribute('innerHTML')
                    energiswap_price_list.append(energiswap_price)
                    
                    #energiswap liquidity tracking
                    energiswap_liquidity_element = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div/div[2]/div/div[3]/div['+str(coin+1)+']/div[1]/div[3]')
                    energiswap_liquidity = energiswap_liquidity_element.get_attribute('innerHTML')
                    energiswap_liquidity_list.append(energiswap_liquidity)
                    
                    esasset_counter = esasset_counter + 1
                    if debugMode == True:
                        print(symbol_output + " " +  str(energiswap_price) + " "  + str(energiswap_liquidity))
            except:
                print("End of list reached.")

            #finds the button to click, then clicks to the next page.
            driver.find_elements_by_xpath("/html/body/div/div/div/div[2]/div/div/div[2]/div/div[4]/div[3]/div")[0].click()

        #closes the driver
        driver.close()

        #turns the giant name string into a list of names with energi and @ removed.
        name_list = name_total_string.replace(" @ Energi","").split("\n")

        #Fixes the name_list with Energi and deletes the last position, which is an empty string
        name_list[0] = 'Energi' 
        del name_list[-1]

        #Tomochain issue is fixed here
        for n,x in enumerate(name_list):
            if x == "Tomochain":
                name_list[n] = "TomoChain"

       

        #symbolIDPuller
        id_list = []
        cgasset_counter = 1
  
        for x in range(len(name_list)):
            for i in range(len(entire_list)):
                if entire_list[i]['name'] == name_list[x].capitalize() or entire_list[i]['name'] == name_list[x] or entire_list[i]['symbol'] == name_list[x].lower() \
                or entire_list[i]['name'] == name_list[x] + " Token" or ((entire_list[i]['symbol'] == symbol_list[x]) and x ==1)\
                or ((entire_list[i]['id'] == "dai") and x==name_list.index("Dai Stablecoin")) or entire_list[i]['name'] == name_list[x] + " Network Token" or entire_list[i]['name'] == name_list[x] + " Crystal Legacy" \
                or ((entire_list[i]['id'] == "tomochain") and x ==name_list.index("TomoChain"))\
                or ((entire_list[i]['id'] == "polymath") and x==name_list.index("Polymath Network")):
                #or ((entire_list[i]['id'] == "hard-protocol") and x==name_list.index("HARD Protocol") + 1):
                    if entire_list[i]['id'] != "litecoin-token" and entire_list[i]['id'] != "san-diego-coin" and (entire_list[i]['id'] != "binance-peg-xrp")and (entire_list[i]['id'] != "binance-peg-eos")and (entire_list[i]['id'] != "pundi-x-2"):  #list of random shit coins that pop up
                        id_list.append(entire_list[i]['id'])
                        cgasset_counter = cgasset_counter + 1
            
       
        #fixes funfair and pundi-x
        id_list.insert(symbol_list.index('fun'),'funfair')
        cgasset_counter = cgasset_counter + 1

        id_list.insert(symbol_list.index('eth'),'ethereum')
        cgasset_counter = cgasset_counter + 1

        del id_list[symbol_list.index('npxs')]
        id_list.insert(symbol_list.index('npxs'),'pundi-x')

        id_list.insert(symbol_list.index('swap'),'trustswap')

        del id_list[symbol_list.index('fun')]
        id_list.insert(symbol_list.index('fun'),'funfair')

        del id_list[symbol_list.index('ant')]
        id_list.insert(symbol_list.index('ant'),'aragon')

        
        print("------------------------", "\n" + str(cgasset_counter), "coingecko assests loaded in")
        print(str(esasset_counter), "energiswap assests loaded in\n")
        

        if cgasset_counter != esasset_counter:
            await discord_coins_to_enter.send("Amount of coins is not correct between coingecko and es, program stopped.")
            if debugMode == False:
                break
        
        some_counter = 1
        if debugMode == True:
            print(id_list,"\n-----------------------------\n",name_list)
            for i in range(len(id_list)):
                try:
                    print(id_list[i],name_list[i],symbol_list[i], some_counter)
                    some_counter = some_counter + 1
                except:
                    print("broken")
            print("WAITING 300 SECONDS")
            time.sleep(300)
        total_request_string = ""
        for i in range(len(id_list)):
            total_request_string = total_request_string + id_list[i] + "%2C"
        total_request_string = total_request_string + "&vs_currencies=usd"
        entire_requeststring = "https://api.coingecko.com/api/v3/simple/price?ids=" + total_request_string

        request = requests.get(entire_requeststring)
        content = request.content

        decoder = content.decode()
        decoded_list = decoder.split(",")

        idname_list_cg = []
        idprice_list_cg = []
        for i in range(len(decoded_list)):
            new = decoded_list[i].strip("\{\}").split(':{"usd"')
            combined = new[0].strip('"') + str(new[1])
            idname_list_cg.append(new[0].strip('"'))
            idprice_list_cg.append(new[1].strip(":"))

        for i in range(len(id_list)):
            idFinder = idname_list_cg.index(id_list[i])
            nameFinder = name_list.index(name_list[i])
            symbolFinder = symbol_list.index(symbol_list[i])
            liquidityFinder = energiswap_liquidity_list.index(energiswap_liquidity_list[i])

            cg_price = float(idprice_list_cg[idFinder])
            profit_percent = (cg_price - float(energiswap_price_list[i].strip("$").replace(",",""))) / ((cg_price + float(energiswap_price_list[i].strip("$").replace(",","")))/2)
            print(" \u001b[37m" + name_list[nameFinder] +"\nsymbol: \t" + symbol_list[symbolFinder] + '\nCoinGecko: \t' + "$" + str(idprice_list_cg[idFinder]) +'\nEnergiSwap: \t' + energiswap_price_list[i] + "\n%Difference: \t", format(profit_percent,'%') + "\nPOSITION #: \t", i+1)
            
            if (profit_percent*100) > user_set_profit and float(energiswap_liquidity_list[liquidityFinder].strip("$").replace(",","")) > liquidity_limit:
                print("\u001b[31mT\u001b[33mr\u001b[32ma\u001b[34md\u001b[36me \u001b[35mF\u001b[31mo\u001b[33mu\u001b[32mn\u001b[34md\u001b[37m")
                await discord_coins_to_enter.send("Name: " + name_list[nameFinder] + "\n" + "ID: " + idname_list_cg[idFinder] +  "\nSymbol: " +symbol_list[symbolFinder]+ "\n\nTrade Difference: " + str(format(profit_percent,'%')) +"\nLiquidity: " + energiswap_liquidity_list[liquidityFinder]+ "\n" + "At time: " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) +"\n-----------------")
                if (profit_percent*100) > ping_alert:
                    await discord_coins_to_enter.send('@everyone')
            print("\n")
        
        name_list.clear(),idname_list_cg.clear(), id_list.clear(), symbol_list.clear(), idprice_list_cg.clear(), energiswap_liquidity_list.clear(), energiswap_price_list.clear(), symbol_list.clear()
    
        time.sleep(60)

client.run(TOKEN)
