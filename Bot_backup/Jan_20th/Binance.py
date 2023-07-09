import pandas as pd
Datas = None

def set_price (file_name):
    globals()['Datas'] = pd.read_csv('Datas\\' + file_name)['PRICE_0'].to_numpy()

def price(number):
    return Datas[number]


def commission_fee(buy, amount):
    if buy == True:
        rate = 0.00015
    else:
        rate = 0.00040
    
    return amount - amount * rate

def buy_sell (money, bought_price, current_price):

    money = commission_fee(True, money)

    change = 1 - (bought_price / current_price)

    change_money = money * change

    money += change_money

    money = commission_fee(False, money)

    return money