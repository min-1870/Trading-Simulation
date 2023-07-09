import imp
import Bot as al
import Trade as bi
import IO
import numpy as np
import pandas as pd


bi.set_price('Datas\\Answers_2021.csv') #Only for Sim


go_combinations = IO.combinations_reader('Go_combinations.csv', 0)
stop_combinations = IO.combinations_reader('Stop_combinations.csv', 0)

def working_manager(Money, K, N, P):
    go_bots = [al.bot() for i in range(len(go_combinations))]
    stop_bots = [al.bot() for i in range(len(stop_combinations))]
    money = Money
    k = K
    n = N
    p = P

    #run the go bots

    #run the stop bots

    for i in range(2190): #Only for sim (for true:)

        #wait 4 hours (In real)

        price = bi.price(i) #Only for sim (sth similar API)

        #update price for all bots

        #gain the profits and winrate from all bots

        #rank bots

        #if better bot exist and you did not bought currently:

            #change bot

        #gain the information about the bot whether bought or not

        #buy or not depends on the above information

        #if sell:
        
            #record which bot you used, and how much you gained.

        #if money below deadline (-20%):

            #break




