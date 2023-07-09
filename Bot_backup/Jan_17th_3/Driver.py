import pandas as pd
import Bot as al
import numpy as np
import time
import random

emas = ['EMA', 'DEMA', 'TEMA']
smas = ['SMA']
others = []

trends = ['UP', 'DOWN', 'UP_DOWN', 'DOWN_UP']

sma_spans = [2, 4]
ema_spans = [2]

#=========== what you can fix ============
money_value = 100
file_name = 'Answers_2021_12.csv'
#=========================================

partial_combinations = []
temp_partial_combinations = []
combinations = []

#========== generate all the possible combinations ==========

for sign_1 in others + smas + emas:
    
    for span_1 in list(set(sma_spans+ema_spans)):

        for trend in trends:

            for sign_2 in others + smas + emas:

                for span_2 in list(set(sma_spans+ema_spans)):

                    partial_combinations.append([sign_1, span_1, trend, sign_2, span_2])
    

#========== filter duplicated & nonsense combinations ==========

for i in range(len(partial_combinations)):
    if partial_combinations[i][0] == 'PRICE':
        partial_combinations[i][1] = 0 #price does not need any value

    if partial_combinations[i][3] == 'PRICE':
        partial_combinations[i][4] = 0 #price does not need any value

    if (partial_combinations[i][0] in smas and partial_combinations[i][1] not in sma_spans) or (partial_combinations[i][0] in emas and partial_combinations[i][1] not in ema_spans):
        partial_combinations[i] = [None, None, None, None, None] 

    if (partial_combinations[i][3] in smas and partial_combinations[i][4] not in sma_spans) or (partial_combinations[i][3] in emas and partial_combinations[i][4] not in ema_spans):
        partial_combinations[i] = [None, None, None, None, None]

    if partial_combinations[i][0] == partial_combinations[i][3] and partial_combinations[i][1] == partial_combinations[i][4]:
        partial_combinations[i] = [None, None, None, None, None] #mark the case has same signs 
    
temp_partial_combinations = partial_combinations[:]
partial_combinations.clear()

for i in temp_partial_combinations:
    if i != [None, None, None, None, None] and i not in partial_combinations:
        partial_combinations.append(i) #remove all nonsense combinations and duplicated combinations

#========== generate full combinations ==========

for i in partial_combinations:
    for j in partial_combinations:
        if i != j: # and i[2] == 'DOWN' and j[2] == 'UP_DOWN' and i[1] > i[4] and j[1] < j[4]
            combinations.append([i,j]) #append only for different buy and sell combinations

random.shuffle(combinations) #spread the combinations
    
#========== time to drive the car ==========

datas = pd.read_csv('Datas\\' + file_name)

al.run_test(100, datas, combinations)




