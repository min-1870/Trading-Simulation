import pandas as pd
import Bot as al

def commission_fee(buy, amount):
    if buy == True:
        rate = 0.00015
    else:
        rate = 0.00040
    
    return amount - amount * rate

def run_test(money_value, file_name, combination):
    '''
    This funtion run the test.
    '''
    df = pd.read_csv(file_name)
    money = money_value

    bought = False
    bought_price = 0

    change = 0 #percentage
    change_money = 0 #amount of money win or lose

    correct = 0

    al.set_combination(combination)

    for i in range(1, len(df.index)):
        '''
        The variable "price" will be updated to the next price in every loop.
        '''
        price = df._get_value(i, 'PRICE')

        al.update_price(price)

        if al.buy() == True:
            bought = True
            bought_price = price
            money = commission_fee(True, money)

            if df._get_value(i, 'ANSWER') == 1:
                correct += 1

        if al.sell() == True and bought == True:
            bought = False
            change = 1 - (bought_price / price)
            change_money = money * change
            money += change_money
            money = commission_fee(False, money)

            if df._get_value(i, 'ANSWER') == -1:
                correct += 1

            if money <= 0:
                money = 0
                break
    
    al.reset()
    
    profit = round(money - money_value, 5)
    winrate = correct / df._get_value(0, 'ANSWER') * 100

    return [profit, winrate, combination[0][0], combination[0][1], combination[0][2], combination[0][3], combination[0][4], combination[1][0], combination[1][1], combination[1][2], combination[1][3], combination[1][4], file_name]