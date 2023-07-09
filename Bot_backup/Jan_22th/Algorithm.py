from queue import PriorityQueue
import Trade as bi
import pandas as pd
import numpy as np
import time as t
import sys


def run_test(money_value, file_name, combinations):
    datas = pd.read_csv('Datas\\' + file_name)
    results_datas = np.empty([len(combinations), 17], dtype = 'object')

    win_average = np.zeros(1000)
    loss_average = np.zeros(1000)
    profits = np.zeros(1000)

    times = np.zeros(10)

    combi_count = 0
    win_count = 0
    loss_count = 0
    save_count = 0

    start_time = 0
    time_count = 0
    time = 0

    combinations_number = len(combinations)
    
    bought_price = 0

    for combination in combinations:
        win_average[:] = np.nan
        loss_average[:] = np.nan
        profits[:] = np.nan

        money = money_value
        bought = False
        profit = 0

        win_count = 0
        loss_count = 0
        month_count = 0
        
        buy_1 = combination[0][0] + '_' + str(combination[0][1])
        buy_2 = combination[0][3] + '_' + str(combination[0][4])
        sell_1 = combination[1][0] + '_' + str(combination[1][1])
        sell_2 = combination[1][3] + '_' + str(combination[1][4])
        
        price_0 = datas['PRICE_0'].to_numpy()
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
                    bought_price = price_0[i]


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
            
                #============================ FINISH TRADE ============================

                if bought == False:

                    profit = bi.buy_sell(money, bought_price, price_0[i]) - money
                    money = bi.buy_sell(money, bought_price, price_0[i])
                    
                    if profit > 0: #save the win
                        win_average[win_count] = profit
                        win_count += 1

                    elif profit < 0: #save the loss
                        loss_average[loss_count] = profit
                        loss_count += 1
                    
                    profits[win_count + loss_count] = profit
                    money = money_value

            
            #============================  EVERY MONTH ===============================
            
            #if i != 0 and i % 183 == 0 or i == len(datas.index)-1: #at every last day of the month

                #month_count += 1
                    
        combi_count += 1

        #============================  EVERY AFTER COMBINATION ===============================

        if win_count != 0 and loss_count != 0 and win_count + loss_count >= 10:#

            win_rate = win_count/(win_count+loss_count) * 100
            loss_rate = 100 - win_rate

            win_avg = np.nanmean(win_average)

            if win_count > 0 and loss_count == 0:
                loss_avg = 0
                results_datas[save_count] = [(win_rate * win_avg) / 12, np.nansum(profits) / 12, win_count+loss_count, win_rate, win_avg, loss_rate, loss_avg, combination[0][0], combination[0][1], combination[0][2], combination[0][3], combination[0][4], combination[1][0], combination[1][1], combination[1][2], combination[1][3], combination[1][4]]
                save_count += 1

            elif win_count > 0 and loss_count > 0:#
                loss_avg = -(np.nanmean(loss_average))
                if (win_rate * (win_avg / loss_avg) - loss_rate) >= 240 and win_avg > loss_avg and loss_rate < win_rate:# and win_rate >= 80 and loss_avg <= 2
                    results_datas[save_count] = [(win_rate * (win_avg / loss_avg) - loss_rate) / 12, np.nansum(profits) / 12, win_count+loss_count, win_rate, win_avg, loss_rate, loss_avg, combination[0][0], combination[0][1], combination[0][2], combination[0][3], combination[0][4], combination[1][0], combination[1][1], combination[1][2], combination[1][3], combination[1][4]]
                    save_count += 1

        if combi_count % 1000 == 0: #extract the result and update the UI
            if combi_count % 10000:
                results = pd.DataFrame(results_datas[range(save_count), :], columns = ['Expect','Profit','Number','Win rate', 'Win average', 'Loss rate', 'Loss average', 'Buy_1', 'Buy_value_1', 'Buy_trend', 'Buy_2', 'Buy_value_2', 'Sell_1', 'Sell_value_1', 'Sell_trend', 'Sell_2', 'Sell_value_2'])
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

    results = pd.DataFrame(results_datas[range(save_count), :], columns = ['Expect','Profit','Number','Win rate', 'Win average', 'Loss rate', 'Loss average',  'Buy_1', 'Buy_value_1', 'Buy_trend', 'Buy_2', 'Buy_value_2', 'Sell_1', 'Sell_value_1', 'Sell_trend', 'Sell_2', 'Sell_value_2'])
    results.to_csv (r'Results' + '_' + file_name[8:12] + '_' + file_name[13:15] + '.csv', index = False, header=True)