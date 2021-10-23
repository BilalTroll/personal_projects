from beta_imports import *
from parameters import *

@client.event
async def on_ready():
    #PRE-REQ REQUIRED HERE
    iteration = 0
    channel = client.get_channel(int(channel_ID))
    while True:
        #MORE COUNTERS
        iteration = iteration +1
        esasset_counter = 0
        name_total_string = ""
        
        await channel.send("**Iteration number: **" + str(iteration))
        energiopener("https://www.energiswap.info/tokens")

        #creates empty lists for usage
        energiswap_liquidity_list = []
        energiswap_price_list = []
        symbol_list = []

        for energiswap_page in range(0,4): #four pages of energiswap
            try:
                for coin in range(50): #50 coins a page
                    
                    #Removed for privacy/copyright reasons.
                    
                    esasset_counter += 1
                    if debugMode == True:
                        print(symbol_output + " " +  str(energiswap_price) + " "  + str(energiswap_liquidity))
            except:
                print("End of list reached.\n")

            #finds the button to click, then clicks to the next page.
            driver.find_elements_by_xpath("/html/body/div/div/div/div[2]/div/div/div[2]/div/div[4]/div[3]/div")[0].click()

        #turns the giant name string into a list of names with energi and @ removed.
        name_list = name_total_string.replace(" @ Energi","").split("\n")
        del name_list[-2:]
        
        id_list = []
        cgasset_counter = 1
        
       #Removed for privacy/copyright reasons.

        if debugMode == True:
            print(name_list,"--------------------------------------------------------------------------------------------------------------------------------------------") 
            print(id_list,"\n")

            somecounter =1
            for i in range(len(id_list)):
                print(name_list[i],id_list[i], somecounter)
                somecounter += 1
        
        print("\nThe amount of energiswap assets: ", esasset_counter)
        print("The amount of coinGecko assets:  ", cgasset_counter)

        if esasset_counter == cgasset_counter:
            print("\u001b[31mC\u001b[32mO\u001b[33mN\u001b[34mT\u001b[35mI\u001b[36mN\u001b[37mU\u001b[32mE \u001b[31mO\u001b[32mP\u001b[33mE\u001b[34mR\u001b[35mA\u001b[36mT\u001b[37mI\u001b[31mO\u001b[34mN\u001b[37m")
        else:
            await channel.send("Amount of coins is not correct, program stopped.")
            print("\u001b[31mAMOUNTS NOT THE SAME.\u001b[37m")
            break

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
                print("\u001b[31mT\u001b[33mr\u001b[32ma\u001b[34md\u001b[36me \u001b[35mF\u001b[31mo\u001b[33mu\u001b[32mn\u001b[34md\u001b[37m\n")
                await channel.send("Name: " + name_list[nameFinder] + "\n" + "ID: " + idname_list_cg[idFinder] +  "\nSymbol: " +symbol_list[symbolFinder]+ "\n\nTrade Difference: " + str(format(profit_percent,'%')) +"\nLiquidity: " + energiswap_liquidity_list[liquidityFinder]+ "\n" + "At time: " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) +"\n-----------------")
                if (profit_percent*100) > ping_alert:
                    await channel.send('@everyone')
            print("\n")
        time.sleep(Iteration_Timer)
client.run(token) 
