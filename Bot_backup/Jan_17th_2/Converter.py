import pandas as pd
import Calculators as cc

tema = cc.TEMA()

def commission_fee(buy, amount):
    if buy == True:
        rate = 0.00015
    else:
        rate = 0.00040
    
    return amount - amount * rate

bought = False
bought_price = 0

money = 100
number = 0
was_buy = False
was_sell = False

df = pd.read_csv('Datas\\'+'BTCUSDT-4h-2021-11.csv')

answers = pd.DataFrame({'ANSWER' : [], 'PRICE' : [], 'TEMA' : []})

answers.at[0] = [0, df.values[0][0], 0]
tema.update_price(df.values[0][0], 2)
for i in range(1, len(df.index)):
    tema.update_price(df.values[i][0], 2)
    answers.at[i] = [0, df.values[i][0], tema.get_result()]


for i in range(1, len(answers.index)-1):

    if was_buy == True:
        
        if bought == False:
            bought = True
            bought_price = df.values[i][0]
            money = commission_fee(bought, money)
        was_buy = False

    if was_sell == True:
        if bought == True:
            bought = False
            change = 1 - (bought_price / df.values[i][0])
            change_money = money * change
            money += change_money
            money = commission_fee(bought, money)
        was_sell = False

    if answers._get_value(i, 'TEMA') < answers._get_value(i-1, 'TEMA') and answers._get_value(i, 'TEMA') < answers._get_value(i+1, 'TEMA'):
        action = 1
        number += 1 
        was_buy = True

    elif answers._get_value(i, 'TEMA') > answers._get_value(i-1, 'TEMA') and answers._get_value(i, 'TEMA') > answers._get_value(i+1, 'TEMA'):
        action = -1
        number += 1 
        was_sell = True


    else:
        action = 0

    answers.at[i] = [action, answers._get_value(i, 'PRICE'), answers._get_value(i, 'TEMA')]

answers.at[len(answers.index)-1] = [0, answers._get_value(len(answers.index)-1, 'PRICE'), answers._get_value(len(answers.index)-1, 'TEMA')]
answers.at[0] = [number , money - 100, 0]

answers.to_csv (r'Answers.csv', index = False, header=True)