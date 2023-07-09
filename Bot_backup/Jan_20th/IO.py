from itertools import count
import pandas as pd
import numpy as np
import Calculators

def answers_writer(file_name):
    SMA_spans = [2, 4, 8, 16, 32, 64, 128]
    EMA_spans = [2, 4, 8, 16, 32, 64, 128]
    DEMA_spans = [2, 4, 8, 16, 32, 64, 128]
    TEMA_spans = [2, 4, 8, 16, 32, 64, 128]
    RSL_spans = [2, 4, 8, 16, 32, 64, 128]
    SPL_spans = [2, 4, 8, 16, 32, 64, 128]
    SMAs = [Calculators.SMA() for i in range(len(SMA_spans))]
    EMAs = [Calculators.EMA() for i in range(len(EMA_spans))]
    DEMAs = [Calculators.DEMA() for i in range(len(DEMA_spans))]
    TEMAs = [Calculators.TEMA() for i in range(len(TEMA_spans))]
    RSLs = [Calculators.RSL() for i in range(len(RSL_spans))]
    SPLs = [Calculators.SPL() for i in range(len(SPL_spans))]

    datas = np.genfromtxt('Datas\\' + file_name, delimiter=',')

    results = []

    answers = pd.DataFrame({'PRICE_0' : [], 'SMA_2' : [], 'SMA_4' : [], 'SMA_8' : [], 'SMA_16' : [], 'SMA_32' : [], 'SMA_64' : [], 'SMA_128' : [], 'EMA_2' : [], 'EMA_4' : [], 'EMA_8' : [], 'EMA_16' : [], 'EMA_32' : [], 'EMA_64' : [], 'EMA_128' : [], 'DEMA_2' : [], 'DEMA_4' : [], 'DEMA_8' : [], 'DEMA_16' : [], 'DEMA_32' : [], 'DEMA_64' : [], 'DEMA_128' : [], 'TEMA_2' : [], 'TEMA_4' : [], 'TEMA_8' : [], 'TEMA_16' : [], 'TEMA_32' : [], 'TEMA_64' : [], 'TEMA_128' : [], 'RSL_2' : [], 'RSL_4' : [], 'RSL_8' : [], 'RSL_16' : [], 'RSL_32' : [], 'RSL_64' : [], 'RSL_128' : [], 'SPL_2' : [], 'SPL_4' : [], 'SPL_8' : [], 'SPL_16' : [], 'SPL_32' : [], 'SPL_64' : [], 'SPL_128' : []})
    
    for i in range(len(datas)):

        for j in range(len(SMA_spans)):
            SMAs[j].update_price(datas[i, 4], SMA_spans[j])
            results.append(SMAs[j].get_result())

        for j in range(len(EMA_spans)):
            EMAs[j].update_price(datas[i, 4], EMA_spans[j])
            results.append(EMAs[j].get_result())

        for j in range(len(DEMA_spans)):
            DEMAs[j].update_price(datas[i, 4], DEMA_spans[j])
            results.append(DEMAs[j].get_result())

        for j in range(len(TEMA_spans)):
            TEMAs[j].update_price(datas[i, 4], TEMA_spans[j])
            results.append(TEMAs[j].get_result())

        for j in range(len(RSL_spans)):
            RSLs[j].update_price(datas[i, 4], RSL_spans[j])
            results.append(RSLs[j].get_result())

        for j in range(len(SPL_spans)):
            SPLs[j].update_price(datas[i, 4], SPL_spans[j])
            results.append(SPLs[j].get_result())

        answers.at[i] = [datas[i, 4]] + results
        results.clear()

    answers.to_csv (r'Answers_2021.csv', index = False, header=True)

def prices_reader(file_name):
    datas = np.genfromtxt(file_name, delimiter=',')
    prices = pd.DataFrame(datas[:, 4], columns = ['PRICE'])
    prices.to_csv (r'Prices' + '_' + file_name[11:15] + '_' + file_name[16:18] + '.csv', index = False, header=True)

def combinations_reader(file_name, g):
    datas = np.genfromtxt(file_name, delimiter=',',dtype = str)
    results = np.empty([len(datas)-1, 2],dtype = 'object')
    count = 0

    for i in datas[range(1, len(datas))]:
        results[count] = [[str(i[0+g]), int(i[1+g]), str(i[2+g]), str(i[3+g]), int(i[4+g])], [str(i[5+g]), int(i[6+g]), str(i[7+g]), str(i[8+g]), int(i[9+g])]]
        count += 1

    return results

def combinations_writer(combinations):

    datas = np.empty([len(combinations), 10], dtype='object')

    for i in range(len(combinations)):
        datas[i] = [combinations[i][0][0], combinations[i][0][1], combinations[i][0][2], combinations[i][0][3], combinations[i][0][4], combinations[i][1][0], combinations[i][1][1], combinations[i][1][2], combinations[i][1][3], combinations[i][1][4]]

    
    results = pd.DataFrame(datas, columns = ['Buy_1', 'Buy_value_1', 'Buy_trend', 'Buy_2', 'Buy_value_2', 'Sell_1', 'Sell_value_1', 'Sell_trend', 'Sell_2', 'Sell_value_2'])
    results.to_csv (r'Combinations.csv', index = False, header=True)

def find_same_combinations(file_names):

    def check_duplicated_list(x, y):
        if x[0][0] == y[0][0] and x[0][1] == y[0][1] and x[0][2] == y[0][2]:
            if x[0][3] == y[0][3] and x[0][4] == y[0][4] and x[1][0] == y[1][0]:
                if x[1][1] == y[1][1] and x[1][2] == y[1][2] and x[1][3] == y[1][3]:
                    if x[1][4] == y[1][4]:
                        return True

    count = 0
    result_datas = np.empty(len(file_names), dtype = 'object')

    for i in range(len(file_names)):
        result_datas[i] = combinations_reader(file_names[i], 1)
    min_index = 0
    
    for i in range(len(result_datas)):
        if len(result_datas[i]) < len(result_datas[min_index]):
            min_index = i

    result = np.empty(len(result_datas[min_index]), dtype = 'object')

    for i in result_datas[min_index]:
        duplicated = 0

        for month in result_datas:

            for combination in month:

                if check_duplicated_list(combination, i):
                    duplicated += 1

                    if duplicated == 6:
                        i = list(i)
                        result[count] = i
                        count += 1
    
    return result[range(count)]

def merge_originals(file_names):

    results_datas = np.empty([2300, 12])
    count = 0

    for file_name in file_names:
        results = np.genfromtxt('Datas\\'+file_name, delimiter=',')

        for result in results:
            results_datas[count] = result
            count+=1
            
    np.savetxt("BTCUSDT_2020.csv", results_datas[range(count)], delimiter=",")

def merge_combinations(combinations1, combinations2):
    return np.vstack((combinations1, combinations2))

    
    