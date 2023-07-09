from queue import PriorityQueue
import Trade as bi
import pandas as pd
import numpy as np
import time as t
import sys


def run_test(money_value, file_name, combinations):
    datas = pd.read_csv('Datas\\' + file_name)
    results_datas = np.empty([len(combinations), 15], dtype = 'object')

    profits = np.zeros(12)
    win_rates = np.zeros(12)
    loss_rates = np.zeros(12)
    win_average = np.zeros(12)
    loss_average = np.zeros(12)

    wins = np.zeros(500)
    losses = np.zeros(500)

    times = np.zeros(10)

    combi_count = 0
    win_count = 0
    loss_count = 0
    start_time = 0
    save_count = 0
    time_count = 0
    life_count = 0

    time = 0

    combinations_number = len(combinations)
    
    bought_price = 0

    for combination in combinations:
        profits[:] = 0
        win_rates[:] = 0
        loss_rates[:] = 0
        win_average[:] = 0
        loss_average[:] = 0
        month_count = 0

        money = money_value
        bought = False
        profit = 0
        
        wins[:] = np.nan
        losses[:] = np.nan
        win_count = 0
        loss_count = 0
        life_count = 0
        
        buy_1 = combination[0][0] + '_' + str(combination[0][1])
        buy_2 = combination[0][3] + '_' + str(combination[0][4])
        sell_1 = combination[1][0] + '_' + str(combination[1][1])
        sell_2 = combination[1][3] + '_' + str(combination[1][4])
        
        buy_1 = datas[buy_1].to_numpy()
        buy_2 = datas[buy_2].to_numpy()
        sell_1 = datas[sell_1].to_numpy()
        sell_2 = datas[sell_2].to_numpy()

        for i in range(len(datas.index)):

            if bought == False:
                try:
                    buy_1_result = buy_1[i]
                    buy_1_pre_result = buy_1[i-1]
                    buy_2_result = buy_2[i]
                    buy_2_pre_result = buy_2[i-1]

                    if buy_1_pre_result < buy_2_pre_result and buy_1_result > buy_2_result:
                        if combination[0][2] == 'ANY':
                            bought = True

                        elif combination[0][3] == 'RSL' or combination[0][3] == 'SPL':
                            if combination[0][2] == 'UP':
                                bought =  buy_1_pre_result < buy_1_result

                            elif combination[0][2] == 'DOWN':
                                bought = buy_1_pre_result > buy_1_result

                        elif combination[0][2] == 'UP':
                            bought =  buy_1_pre_result < buy_1_result and buy_2_pre_result < buy_2_result

                        elif combination[0][2] == 'DOWN':
                            bought = buy_1_pre_result > buy_1_result and buy_2_pre_result > buy_2_result
                        
                        elif combination[0][2] == 'UP_DOWN':
                            bought = buy_1_pre_result < buy_1_result and buy_2_pre_result > buy_2_result

                except:
                    bought = False
            
                if bought == True:
                    bought_price = datas._get_value(i, 'PRICE_0')


            elif bought == True:
                try:
                    sell_1_result = sell_1[i]
                    sell_1_pre_result = sell_1[i-1]
                    sell_2_result = sell_2[i]
                    sell_2_pre_result = sell_2[i-1]

                    if sell_1_pre_result < sell_2_pre_result and sell_1_result > sell_2_result:
                        if combination[1][2] == 'ANY':
                            bought = True

                        elif combination[1][3] == 'RSL' or combination[1][3] == 'SPL':
                            if combination[1][2] == 'UP':
                                bought =  sell_1_pre_result < sell_2_result

                            elif combination[1][2] == 'DOWN':
                                bought = sell_1_pre_result > sell_2_result

                        elif combination[1][2] == 'UP':
                            bought =  not(sell_1_pre_result < sell_1_result and sell_2_pre_result < sell_2_result)

                        elif combination[1][2] == 'DOWN':
                            bought = not(sell_1_pre_result > sell_1_result and sell_2_pre_result > sell_2_result)
                        
                        elif combination[1][2] == 'UP_DOWN':
                            bought = not(sell_1_pre_result < sell_1_result and sell_2_pre_result > sell_2_result)

                except:
                    bought = True
            
                #============================ every deal ============================

                if bought == False:
                    money = bi.buy_sell(money, bought_price, datas._get_value(i, 'PRICE_0'))
                    profit = money - 100

                    if profit > 0: #save the win
                        wins[win_count] = profit
                        win_count += 1

                    elif profit < 0: #save the loss
                        losses[loss_count] = profit
                        loss_count += 1
            
            #============================  EVERY MONTH ===============================
            
            if i != 0 and i % 183 == 0 or i == len(datas.index)-1: #at every last day of the month

                if win_count == 0 and loss_count >= 0: #if no deal or only loss has been made, break it
                    break
                
                elif loss_count == 0: #if never loss money, you will only gain money!!!!!!
                    win_rates[month_count] = 100
                    loss_rates[month_count] = 0
                    win_average[month_count] = round(np.nanmean(wins), 2)
                    loss_average[month_count] = 0

                    profits[month_count] = win_average[month_count]

                elif (np.nanmean(wins) / np.nanmean(losses)) > ((loss_count / (win_count + loss_count)) / (win_count / (win_count + loss_count))):
                    win_rates[month_count] = round(win_count / (win_count + loss_count) * 100, 2)
                    loss_rates[month_count] = round(loss_count / (win_count + loss_count) * 100, 2)
                    win_average[month_count] = round(np.nanmean(wins), 2)
                    loss_average[month_count] = round(np.nanmean(losses), 2)

                    profits[month_count] = (win_average[month_count] / loss_average[month_count]) - (loss_rates[month_count] / win_rates[month_count])
                
                else:
                    if life_count < 6:
                        win_rates[month_count] = round(win_count / (win_count + loss_count) * 100, 2)
                        loss_rates[month_count] = round(loss_count / (win_count + loss_count) * 100, 2)
                        win_average[month_count] = round(np.nanmean(wins), 2)
                        loss_average[month_count] = round(np.nanmean(losses), 2)
                        
                        profits[month_count] = (win_average[month_count] / loss_average[month_count]) - (loss_rates[month_count] / win_rates[month_count])

                    else:
                        break

                    life_count += 1

                month_count += 1

                #========================  values I have to reset every month ====================

                money = money_value
                bought = False
                profit = 0
                
                wins[:] = np.nan
                losses[:] = np.nan
                win_count = 0
                loss_count = 0
                    
        combi_count += 1

        #============================  EVERY AFTER COMBINATION ===============================

        if month_count == 12: #if all 12 month gained profit
            results_datas[save_count] = [np.mean(profits), np.mean(win_rates), np.mean(win_average), np.mean(loss_rates), np.mean(loss_average), combination[0][0], combination[0][1], combination[0][2], combination[0][3], combination[0][4], combination[1][0], combination[1][1], combination[1][2], combination[1][3], combination[1][4]]
            save_count += 1

        if combi_count % 1000 == 0: #extract the result and update the UI
            results = pd.DataFrame(results_datas[range(save_count), :], columns = ['Profit','Win rate', 'Win average', 'Loss rate', 'Loss average', 'Buy_1', 'Buy_value_1', 'Buy_trend', 'Buy_2', 'Buy_value_2', 'Sell_1', 'Sell_value_1', 'Sell_trend', 'Sell_2', 'Sell_value_2'])
            results.to_csv (r'Results' + '_' + file_name[8:12] + '_' + file_name[13:15] + '.csv', index = False, header=True)

            left = combinations_number - combi_count
            progress = int((100 / combinations_number) * combi_count)

            if combi_count != 1:
                spending_time = (t.time() - start_time) / 1000
                times[time_count % 10] = int((left) * spending_time / 60)
                time = np.nanmean(times[times != 0])
                time_count += 1
            start_time = t.time()

            sys.stdout.write("\033[F") #back to previous line 
            sys.stdout.write("\033[K") #clear line 
            print('#' + str(left) + '   PROGRESS : ' + str(progress) + '%       ' + str(time) + ' minutes left..' )

    results = pd.DataFrame(results_datas[range(save_count), :], columns = ['Profit','Win rate', 'Win average', 'Loss rate', 'Loss average',  'Buy_1', 'Buy_value_1', 'Buy_trend', 'Buy_2', 'Buy_value_2', 'Sell_1', 'Sell_value_1', 'Sell_trend', 'Sell_2', 'Sell_value_2'])
    results.to_csv (r'Results' + '_' + file_name[8:12] + '_' + file_name[13:15] + '.csv', index = False, header=True)