from pycoingecko import CoinGeckoAPI
import requests
import discord

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options

import os
import time

#token for bot.
TOKEN = "ODQ4MzA2NzEyMTc2MDk5MzM4.YLKtMA.cRIFiTFGpq-dzVg3uGZP-fEeBYg"

#starts discord
client = discord.Client()

iteration = 0

#Enter this as a percentage. It's how close the energiswap and cg price must be to execute.
tolerance = 2

debugMode = False

symbol_user_list = []
symbol_user_amount = int(input("Enter the amount of symbols you want to check: "))

for i in range(0,symbol_user_amount):
    symbol_user = str(input("Enter the symbol of the coin: "))
    symbol_user_list.append(symbol_user)
    
@client.event
async def on_ready():
    print("Connected")

    discord_coins_to_exit = client.get_channel(870778011249700864)

    while True:
        global iteration
        iteration = iteration + 1

        #add's color to system
        os.system("cls")
        cg = CoinGeckoAPI()
        ts = time.gmtime()

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        symbol_total_string = ""
        name_total_string = ""
        combined_string = ""
        energiswap_price_total = ""
        

        esasset_counter = 0
        entire_list = cg.get_coins_list()

        #prepares path for driver and window size. Must take up at least half of screen.
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH,options=chrome_options)
        driver.set_window_size(1920,1080)

        #chrome driver opens energi-swap main site, then sleeps to fully open webpage.
        driver.get("https://www.energiswap.info/tokens")
        time.sleep(3.5) #DO NOT TOUCH THIS.

        for energiswap_page in range(0,4): #four pages of energiswap
            try:
                for coin in range(50): #50 coins a page
                    symbol_element = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div/div[2]/div/div[3]/div['+str(coin+1)+']/div[1]/div[2]/div')

                    if len(symbol_element.get_attribute('innerHTML')) > 20: #checks to see if the output would be really long(BADGER ISSUE), if it is, go one division further.
                        symbol_element = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div/div[2]/div/div[3]/div['+str(coin+1)+']/div[1]/div[2]/div/div')
                        
                    #the symbol_element outputs the element line, we want the inner information -> symbol_output
                    symbol_output = symbol_element.get_attribute('innerHTML')
                    symbol_total_string = symbol_total_string + " " + symbol_output.lower()

                    #Scrapes name of coin
                    name_element = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div/div[2]/div/div[3]/div['+str(coin+1) +']/div[1]/div[1]/div/a/div')
                    if len(name_element.get_attribute('innerHTML')) > 20:
                        name_element = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div/div[2]/div/div[3]/div[' + str(coin+1) +']/div[1]/div[1]/div/a/div/div')

                    name_output = name_element.get_attribute('innerHTML')
                    name_total_string = name_total_string +  name_output + "\n"

                    energiswap_price_element = driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div/div[2]/div/div[3]/div['+ str(coin+1) +']/div[1]/div[5]')
                    energiswap_price = energiswap_price_element.get_attribute('innerHTML')
                    energiswap_price_total = energiswap_price_total + str(energiswap_price) + "\n"

                    esasset_counter = esasset_counter + 1
                    #print(symbol_output + " " + str(energiswap_price))
            except:
                print("End of list reached.")

            #finds the button to click, then clicks to the next page.
            driver.find_elements_by_xpath("/html/body/div/div/div/div[2]/div/div/div[2]/div/div[4]/div[3]/div")[0].click()

        #closes the driver
        driver.close()

         #turns the giant symbol string into a symbol list in the order it is gathered from energiswap.
        symbol_list = symbol_total_string.split()
        #turns the giant name string into a list of names with energi and @ removed.
        name_list = name_total_string.replace(" @ Energi","").split("\n")

        #takes the prices and splits them into a list where the indexes are equal to those of the names and ids.
        energiswap_price_list = energiswap_price_total.split()

        #Fixes the name_list with Energi and deletes the last position, which is an empty string
        name_list[0] = 'Energi' 
        del name_list[-1]

        #Tomochain issue is fixed here
        for n,x in enumerate(name_list):
            if x == "Tomochain":
                name_list[n] = "TomoChain"

        #symbolIDPuller
        id_list = []
        cgasset_counter = 2
  
        for x in range(len(name_list)):
            for i in range(len(entire_list)):
                if entire_list[i]['name'] == name_list[x].capitalize() or entire_list[i]['name'] == name_list[x] or entire_list[i]['symbol'] == name_list[x].lower() \
                or entire_list[i]['name'] == name_list[x] + " Token" or ((entire_list[i]['symbol'] == symbol_list[x]) and x ==1)\
                or ((entire_list[i]['id'] == "dai") and x==name_list.index("Dai Stablecoin")) or entire_list[i]['name'] == name_list[x] + " Network Token" or entire_list[i]['name'] == name_list[x] + " Crystal Legacy" \
                or ((entire_list[i]['id'] == "tomochain") and x ==name_list.index("TomoChain"))\
                or ((entire_list[i]['id'] == "polymath") and x==name_list.index("Polymath Network"))\
                or ((entire_list[i]['id'] == "hard-protocol") and x==name_list.index("HARD Protocol") + 1):
                    if entire_list[i]['id'] != "litecoin-token" and entire_list[i]['id'] != "san-diego-coin" and (entire_list[i]['id'] != "binance-peg-xrp")and (entire_list[i]['id'] != "binance-peg-eos")and (entire_list[i]['id'] != "pundi-x-2"):  #list of random shit coins that pop up
                        id_list.append(entire_list[i]['id'])
                        cgasset_counter = cgasset_counter + 1
            
        print("------------------------", "\n" + str(cgasset_counter), "coingecko assests loaded in")
        print(str(esasset_counter), "energiswap assests loaded in\n")

        #fixes funfair and pundi-x
        id_list.insert(symbol_list.index('fun'),'funfair')
        cgasset_counter = cgasset_counter + 1

        id_list.insert(symbol_list.index('eth'),'ethereum')
        cgasset_counter = cgasset_counter + 1

        del id_list[symbol_list.index('npxs')]
        id_list.insert(symbol_list.index('npxs'),'pundi-x')
        cgasset_counter = cgasset_counter + 1


        some_counter = 1
        if debugMode == True:
            print(id_list,"\n-----------------------------\n",name_list)
            for i in range(len(id_list)):
                try:
                    print(id_list[i],name_list[i],some_counter)
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
            try:
                combined = new[0].strip('"') + str(new[1])
            except:
                continue
            idname_list_cg.append(new[0].strip('"'))
            idprice_list_cg.append(new[1].strip(":"))

        print("\u001b[31mTolerance is: \u001b[37m", tolerance)
        for x in range(symbol_user_amount):
            for i in range(len(id_list)):
                
                idFinder = idname_list_cg.index(id_list[i])
                nameFinder = name_list.index(name_list[i])
                symbolFinder = symbol_list.index(symbol_list[i])

            
                cg_price = float(idprice_list_cg[idFinder])
                profit_percent = (cg_price - float(energiswap_price_list[i].strip("$").replace(",",""))) / ((cg_price + float(energiswap_price_list[i].strip("$").replace(",","")))/2) * 100

                if((symbol_list[i] == symbol_user_list[x]) or symbol_list[i] == symbol_user_list[x].lower()):
                    #print(symbol_list[i], idprice_list_cg[idFinder], energiswap_price_list[i].strip("$"))
                    
                    print("Name: " + name_list[nameFinder] + "\nSymbol: " +symbol_list[symbolFinder]  + "\n\nCoinGecko: $" + str(idprice_list_cg[idFinder])  + "\nEnergiswap: " + str(energiswap_price_list[i]) + "\nTolerance: " +str(profit_percent) +"\n\n" + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) +"\n-----------------")
                    
                    
                    if((profit_percent < tolerance) or profit_percent < tolerance*-1):
                        print(symbol_list[i], idprice_list_cg[idFinder], energiswap_price_list[i].strip("$"))
                        print("\u001b[31mT\u001b[33mr\u001b[32ma\u001b[34md\u001b[36me \u001b[35mF\u001b[31mo\u001b[33mu\u001b[32mn\u001b[34md \u001b[37m:",profit_percent)
                        print("\n")

                        await discord_coins_to_exit.send("**Name: **" + name_list[nameFinder] + "\nSymbol: " +symbol_list[symbolFinder]  + "\n\nCoinGecko: $" + str(idprice_list_cg[idFinder])  + "\nEnergiswap: " + str(energiswap_price_list[i]) + "\nTolerance: " +str(profit_percent) +"\n\n" + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) +"\n-----------------")
                        await discord_coins_to_exit.send("@everyone")
        print("\u001b[31mSLEEPING 60 SECONDS\u001b[37m")
        time.sleep(60)


client.run(TOKEN)
