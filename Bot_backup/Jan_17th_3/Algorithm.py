import Trade as bi
import pandas as pd
import numpy as np
import sys

def run_test(money_value, datas, combinations):
    results = pd.DataFrame({'Profit (%)' : [], 'Buy_1' : [], 'Buy_value_1' : [], 'Buy_trend' : [], 'Buy_2' : [], 'Buy_value_2' : [], 'Sell_1' : [], 'Sell_value_1' : [], 'Sell_trend' : [], 'Sell_2' : [], 'Sell_value_2' : []})
    count = 0
    combinations_number = len(combinations)

    for combination in combinations:
        money = money_value
        bought_price = 0

        buy_sign_1 = combination[0][0] + '_' + str(combination[0][1])
        buy_sign_2 = combination[0][3] + '_' + str(combination[0][4])
        sell_sign_1 = combination[1][0] + '_' + str(combination[1][1])
        sell_sign_2 = combination[1][3] + '_' + str(combination[1][4])

        bought = False

        for i in range(len(datas.index)):

            if bought == False:
                try:
                    buy_sign_1_result = datas._get_value(i, buy_sign_1)
                    buy_sign_1_pre_result = datas._get_value(i-1, buy_sign_1)
                    buy_sign_2_result = datas._get_value(i, buy_sign_2)
                    buy_sign_2_pre_result = datas._get_value(i-1, buy_sign_2)

                    if buy_sign_1_pre_result < buy_sign_2_pre_result and buy_sign_1_result > buy_sign_2_result:

                        if combination[0][2] == 'UP':
                            bought =  buy_sign_1_pre_result < buy_sign_1_result and buy_sign_2_pre_result < buy_sign_2_result

                        elif combination[0][2] == 'DOWN':
                            bought = buy_sign_1_pre_result > buy_sign_1_result and buy_sign_2_pre_result > buy_sign_2_result
                        
                        elif combination[0][2] == 'UP_DOWN':
                            bought = buy_sign_1_pre_result < buy_sign_1_result and buy_sign_2_pre_result > buy_sign_2_result
                        
                        elif combination[0][2] == 'DOWN_UP':
                            bought = buy_sign_1_pre_result > buy_sign_1_result and buy_sign_2_pre_result < buy_sign_2_result

                except:
                    bought = False
            
                if bought == True:
                    bought_price = datas._get_value(i, 'PRICE')


            elif bought == True:
                try:
                    sell_sign_1_result = datas._get_value(i, sell_sign_1)
                    sell_sign_1_pre_result = datas._get_value(i-1, sell_sign_1)
                    sell_sign_2_result = datas._get_value(i, sell_sign_2)
                    sell_sign_2_pre_result = datas._get_value(i-1, sell_sign_2)

                    if sell_sign_1_pre_result < sell_sign_2_pre_result and sell_sign_1_result > sell_sign_2_result:

                        if combination[1][2] == 'UP':
                            bought =  not(sell_sign_1_pre_result < sell_sign_1_result and sell_sign_2_pre_result < sell_sign_2_result)

                        elif combination[1][2] == 'DOWN':
                            bought = not(sell_sign_1_pre_result > sell_sign_1_result and sell_sign_2_pre_result > sell_sign_2_result)
                        
                        elif combination[1][2] == 'UP_DOWN':
                            bought = not(sell_sign_1_pre_result < sell_sign_1_result and sell_sign_2_pre_result > sell_sign_2_result)
                        
                        elif combination[1][2] == 'DOWN_UP':
                            bought = not(sell_sign_1_pre_result > sell_sign_1_result and sell_sign_2_pre_result < sell_sign_2_result)

                except:
                    bought = True
            
                if bought == False:
                    money = bi.buy_sell(money, bought_price, datas._get_value(i, 'PRICE'))

        results.at[len(results.index)] = [money - 100, combination[0][0], combination[0][1], combination[0][2], combination[0][3], combination[0][4], combination[1][0], combination[1][1], combination[1][2], combination[1][3], combination[1][4]]
        count += 1
        
        left = combinations_number - count
        progress = int((100 / combinations_number) * count)
        time = int((left) * 0.0003)   
        sys.stdout.write("\033[F") #back to previous line 
        sys.stdout.write("\033[K") #clear line 
        print('#' + str(left) + '   PROGRESS : ' + str(progress) + '%       ' + str(time) + ' minutes left..')

        if count % 1000 == 0:
            results.to_csv (r'Simulation_results.csv', index = False, header=True)

    results.to_csv (r'Simulation_results.csv', index = False, header=True)