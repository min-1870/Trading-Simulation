import numpy as np
import IO

#class init / buy or sell / bought price / winrate / win avg/ loss avg
class bot:

    def __init__(self, combination, saving_limit):
        #variable for trading
        self.combination = combination
        self.saving_limit = saving_limit
        self.bought = False
        self.bought_price = 0

        #variable for winner
        self.wins = np.empty(saving_limit)
        self.wins[:] = np.nan
        self.wins_count = 0
        self.win_rate = 0
        self.wins_losses_record = np.empty(saving_limit)
        self.wins_losses_record[:] = np.nan
        self.trade_count = 0

        #variable for losser
        self.losses = np.empty(saving_limit)
        self.losses[:] = np.nan
        self.losses_count = 0

        #saving trend
        self.buy_trend = self.combination[0][2]
        self.sell_trend = self.combination[1][2]

        #saving pre_results
        self.pre_results = [None, None, None, None]

    def update(self, price, results):
        #print(results)
        
        #decide whether to trade or not
        if self.bought == False:

            try:
                buy_1_result = results[0]
                buy_1_pre_result = self.pre_results[0]
                buy_2_result = results[1]
                buy_2_pre_result = self.pre_results[1]
                if buy_1_pre_result < buy_2_pre_result and buy_1_result > buy_2_result:
                    if self.buy_trend == 'ANY':
                        self.bought = True

                    elif self.combination[0][3] == 4 or self.combination[0][3] == 5:
                        if self.buy_trend == 'UP':
                            self.bought =  buy_1_pre_result < buy_1_result

                        elif self.buy_trend == 'DOWN':
                            self.bought = buy_1_pre_result > buy_1_result

                    elif self.buy_trend == 'UP':
                        self.bought =  buy_1_pre_result < buy_1_result and buy_2_pre_result < buy_2_result

                    elif self.buy_trend == 'DOWN':
                        self.bought = buy_1_pre_result > buy_1_result and buy_2_pre_result > buy_2_result
                        
                    elif self.buy_trend == 'UP_DOWN':
                        self.bought = buy_1_pre_result < buy_1_result and buy_2_pre_result > buy_2_result

            except:
                self.bought = False
            
            self.pre_results[0], self.pre_results[1], self.pre_results[2], self.pre_results[3] = results[0], results[1], results[2], results[3]

            if self.bought == True:
                self.bought_price = price

                return True #return trading decision

        elif self.bought == True:
            try:
                sell_1_result = results[2]
                sell_1_pre_result = self.pre_results[2]
                sell_2_result = results[3]
                sell_2_pre_result = self.pre_results[3]

                if sell_1_pre_result < sell_2_pre_result and sell_1_result > sell_2_result:
                    if self.sell_trend == 'ANY':
                        self.bought = True

                    elif self.combination[1][3] == 'RSL' or self.combination[1][3] == 'SPL':
                        if self.sell_trend == 'UP':
                            self.bought =  sell_1_pre_result < sell_2_result

                        elif self.sell_trend == 'DOWN':
                            self.bought = sell_1_pre_result > sell_2_result

                    elif self.sell_trend == 'UP':
                        self.bought =  not(sell_1_pre_result < sell_1_result and sell_2_pre_result < sell_2_result)

                    elif self.sell_trend == 'DOWN':
                        self.bought = not(sell_1_pre_result > sell_1_result and sell_2_pre_result > sell_2_result)
                        
                    elif self.sell_trend == 'UP_DOWN':
                        self.bought = not(sell_1_pre_result < sell_1_result and sell_2_pre_result > sell_2_result)

            except:
                self.bought = True
            
            self.pre_results[0], self.pre_results[1], self.pre_results[2], self.pre_results[3] = results[0], results[1], results[2], results[3]
            #============================ FINISH TRADE ============================

            if self.bought == False:

                profit = (1 - self.bought_price / price) * 100
                    
                if profit > 0: #save the win
                    self.wins[self.wins_count % self.saving_limit] = profit
                    self.wins_count += 1
                    self.wins_losses_record[self.trade_count] = 1

                elif profit < 0: #save the loss
                    self.losses[self.losses_count % self.saving_limit] = profit * -1
                    self.losses_count += 1
                    self.wins_losses_record[self.trade_count % self.saving_limit] = 0

                self.trade_count += 1

                return False #return trading decision
        
        self.pre_results[0], self.pre_results[1], self.pre_results[2], self.pre_results[3] = results[0], results[1], results[2], results[3]

        return None #return trading decision

    def get_combination(self):
        return self.combination

    def get_summary(self):
        
        if self.trade_count != 0:
            if self.wins_count == 0:
                win_avg = 0
            else: 
                win_avg = round(np.nanmean(self.wins), 3)

            if self.losses_count == 0:
                loss_avg = 0
            else: 
                loss_avg = round(np.nanmean(self.losses), 3)

            profit = round(np.nansum(self.wins) + np.nansum(self.losses), 3)
            win_rate = round(np.nanmean(self.wins_losses_record) * 100, 3)
            loss_rate = round(100 - win_rate, 3)
            expect = round((win_rate * (win_avg / loss_avg) - loss_rate), 3)
            combintaion = IO.num_2_sign(self.combination)

        else:
            profit = 0
            win_rate = 0
            win_avg = 0
            loss_rate = 0
            loss_avg = 0
            expect = 0
            combintaion = IO.num_2_sign(self.combination)

        return [expect, profit, self.trade_count, win_rate, win_avg, loss_rate, loss_avg, combintaion[0][0], combintaion[0][1], combintaion[0][2], combintaion[0][3], combintaion[0][4], combintaion[1][0], combintaion[1][1], combintaion[1][2], combintaion[1][3], combintaion[1][4]]
