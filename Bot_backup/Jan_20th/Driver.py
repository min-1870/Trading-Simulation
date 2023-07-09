from itertools import combinations
import pandas as pd
import Bot as al
import IO
import random

def generate_all_combinations(Smas, Sma_spans, Emas, Ema_spans, Lines, Lines_spans, Others, Trends):
    smas = Smas
    sma_spans = Sma_spans
    emas = Emas
    ema_spans = Ema_spans
    lines = Lines
    line_spans = Lines_spans
    others = Others
    trends = Trends

    partial_combinations = []
    temp_partial_combinations = []
    combinations = []

    #========== generate all the possible combinations ==========

    for sign_1 in smas + emas + lines + others:
        
        for span_1 in list(set(sma_spans+ema_spans+line_spans)):

            for trend in trends:

                for sign_2 in smas + emas + lines + others:

                    for span_2 in list(set(sma_spans+ema_spans+line_spans)):

                        partial_combinations.append([sign_1, span_1, trend, sign_2, span_2])
        

    #========== filter duplicated & nonsense combinations ==========

    for i in range(len(partial_combinations)):
        if partial_combinations[i][0] == 'PRICE':
            partial_combinations[i][1] = 0 #price does not need any value

        if partial_combinations[i][3] == 'PRICE':
            partial_combinations[i][4] = 0 #price does not need any value

        if partial_combinations[i][0] in  lines:
            partial_combinations[i] = [None, None, None, None, None]

        if partial_combinations[i][3] in  lines and partial_combinations[i][3] == 'UP_DOWN':
            partial_combinations[i] = [None, None, None, None, None]

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
            if i != j: #and ('PRICE' in i or 'PRICE' in j)
                combinations.append([i,j]) #append only for different buy and sell combinations

    random.shuffle(combinations) #spread the combinations

    return combinations
    
#========== time to drive the car ==========

Emas = ['EMA', 'DEMA', 'TEMA'] #
Smas = ['SMA']
Others = ['PRICE']
Lines = ['RSL', 'SPL']

Trends = ['UP', 'DOWN', 'UP_DOWN', 'ANY']

Sma_spans = [2, 4, 8, 16, 32, 64, 128]
Ema_spans = [2, 4, 8, 16, 32, 64, 128]
Lines_spans = [2, 4, 8, 16, 32, 64, 128]

money_value = 100
R_dir = 'Results_backup\\'
D_dir = 'Datas\\'

Results_file_names = ['Results_2021_01.csv', 'Results_2021_02.csv', 'Results_2021_03.csv', 'Results_2021_04.csv', 'Results_2021_05.csv', 'Results_2021_06.csv', 'Results_2021_07.csv', 'Results_2021_08.csv', 'Results_2021_09.csv', 'Results_2021_10.csv', 'Results_2021_11.csv', 'Results_2021_12.csv']
Datas_file_names = ['Answers_2021_01.csv', 'Answers_2021_02.csv', 'Answers_2021_03.csv', 'Answers_2021_04.csv', 'Answers_2021_05.csv', 'Answers_2021_06.csv', 'Answers_2021_07.csv', 'Answers_2021_08.csv', 'Answers_2021_09.csv', 'Answers_2021_10.csv', 'Answers_2021_11.csv', 'Answers_2021_12.csv']
Originals_file_names = ['BTCUSDT-4h-2021-01.csv', 'BTCUSDT-4h-2021-02.csv', 'BTCUSDT-4h-2021-03.csv', 'BTCUSDT-4h-2021-04.csv', 'BTCUSDT-4h-2021-05.csv', 'BTCUSDT-4h-2021-06.csv', 'BTCUSDT-4h-2021-07.csv', 'BTCUSDT-4h-2021-08.csv', 'BTCUSDT-4h-2021-09.csv', 'BTCUSDT-4h-2021-10.csv', 'BTCUSDT-4h-2021-11.csv', 'BTCUSDT-4h-2021-12.csv']
Old_originals_file_names = ['BTCUSDT-4h-2020-01.csv', 'BTCUSDT-4h-2020-02.csv', 'BTCUSDT-4h-2020-03.csv', 'BTCUSDT-4h-2020-04.csv', 'BTCUSDT-4h-2020-05.csv', 'BTCUSDT-4h-2020-06.csv', 'BTCUSDT-4h-2020-07.csv', 'BTCUSDT-4h-2020-08.csv', 'BTCUSDT-4h-2020-09.csv', 'BTCUSDT-4h-2020-10.csv', 'BTCUSDT-4h-2020-11.csv', 'BTCUSDT-4h-2020-12.csv']

#IO.save_combinations(IO.find_same_combinations(Results_file_names))
#generate_all_combinations(Smas, Sma_spans, Emas, Ema_spans, Lines, Lines_spans, Others, Trends)
#for file_name in Datas_file_names:
#for file_name in Originals_file_names:
#IO.answers_writer('BTCUSDT_2020.csv')
#IO.merge_originals(Originals_file_names)
#IO.merge_combinations(IO.combinations_reader('Combinations.csv', 0), IO.combinations_reader('Results_2021_cs.csv', 1)

al.run_test(100, 'Answers_2021.csv', generate_all_combinations(Smas, Sma_spans, Emas, Ema_spans, Lines, Lines_spans, Others, Trends))
#IO.combinations_writer(IO.combinations_reader('Results_2021_cs.csv', 1))

