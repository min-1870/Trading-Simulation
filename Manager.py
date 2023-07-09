import Bot
import Trade
import IO
import numpy as np
import Calculators as cl
import pandas as pd
import sys
import time

binance = Trade.binance('Datas\\Answers_2021.csv')

def working_manager(Money, Combinations, Saving_limit):
    combinations = IO.signs_2_nums(Combinations) #changing signs into numbers
    bots = [Bot.bot(combination, Saving_limit) for combination in combinations]
    history = np.empty((5000, 3))
    trues =  0
    falses = 0
    nones = 0
    money = Money
    start_time = time.time()

    main_count = 0
    save_count = 0
    main_results = np.empty((len(combinations), 17), dtype=object)

    #temp variable for input and output in each bot
    input_results = np.empty(4)
    input_results[:] = None
    output_result = None
    
    #count the spans for each signs
    sign_spans = IO.sign_spans(combinations)
    max_span = np.amax(sign_spans) + 1

    #create objects
    calculators = np.empty(6, dtype=object)
    calculators[0] = [cl.PRICE(i) for i in range(max_span)]
    calculators[1] = [cl.SMMA(i) for i in range(max_span)]
    calculators[2] = [cl.EMA(i) for i in range(max_span)]
    calculators[3] = [cl.SMA(i) for i in range(max_span)]
    calculators[4] = [cl.RSL(i) for i in range(max_span)]
    calculators[5] = [cl.SPL(i) for i in range(max_span)]

    #result of pre calc
    calc_results = np.empty((6, max_span))

    while True:

        #wait 4 hours (In real)

        price = binance.get_price() #Only for sim (sth similar API)
        if price == None: break

        #precalculate every results
        for i in range(len(calculators)):
            for j in sign_spans[i, :]:
                if j == -1: break
                calculators[i][j].update_price(price)
                calc_results[i, j] = calculators[i][j].get_result()

        #update value for all bots
        for bot in bots:

            #using precalculated results assign into each bot and bring back result
            combination = bot.get_combination()

            c = 0
            for buy_sell_index in [0, 1]:
                for sign_index in [0, 3]:
                    sign = combination[buy_sell_index][sign_index]
                    span = combination[buy_sell_index][sign_index+1]
                    input_results[c] = calc_results[sign, span]
                    
                    c += 1

            output_result = bot.update(price, input_results)

            if output_result == True:
                trues += 1
            
            elif output_result == False:
                falses += 1

            else:
                nones += 1

        #record the results from bots
        history[main_count] = [trues, falses, nones]
        trues, falses, nones = 0,0,0

        #UI
        if main_count % 100 == 0:

            remain_update = 3000 - main_count
            remain_time = (time.time() - start_time / 100) * remain_update
            progress = int((100 / 3000) * main_count)

            sys.stdout.write("\033[F") #back to previous line 
            sys.stdout.write("\033[K") #clear line 
            print('#' + str(remain_update) + '   PROGRESS : ' + str(progress) + '%       ' + str(remain_time) + ' minutes left..' )
            start_time = time.time()

        main_count += 1

    #gathering summaries
    for bot in bots:
        result = bot.get_summary()

        if filter(result):
            main_results[save_count] = result
            save_count += 1
        
    #save them
    results = pd.DataFrame(main_results[range(save_count), :], columns = ['Expect','Profit','Trade','Win rate', 'Win AVG', 'Loss rate', 'Loss AVG',  'Buy_1', 'Buy_value_1', 'Buy_trend', 'Buy_2', 'Buy_value_2', 'Sell_1', 'Sell_value_1', 'Sell_trend', 'Sell_2', 'Sell_value_2'])
    results.to_csv (r'Results.csv', index = False, header=True)

def filter(data):
    result = False

    if True:
        result = True

    return result

working_manager(100, [[['SMA', 64, 'ANY', 'RSL', 4],['SMA', 2, 'UP_DOWN', 'SMA', 8]],[['PRICE', 0, 'UP', 'PRICE', 0],['PRICE', 0, 'UP', 'PRICE', 0]]], 3000)



























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




