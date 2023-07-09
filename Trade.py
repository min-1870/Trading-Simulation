import numpy as np


class binance:
    
    def __init__(self, file_name) -> None:
        self.datas = np.genfromtxt(file_name, delimiter=',')[1:,0]
        self.count = 0 

    def get_price(self):

        if self.count == len(self.datas):
            return None

        result = self.datas[self.count]
        self.count += 1
        return result


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