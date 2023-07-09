import pandas as pd
import numpy as np

def answers_writer(file_name, period):
    datas = np.genfromtxt(file_name, delimiter=',', dtype='float32')
    prices = datas[8:,3]
    result = np.zeros((len(prices) - period + 1, period))

    for i in range(len(prices) - period + 1):
        result[i] = [prices[j+i] for j in range(period)]

        if result[i,period-2] < result[i,period-1]:
            result[i,period-1] = 1

        else:
            result[i,period-1] = 0

    result = np.asarray(result).astype('float32')
        
    #np.savetxt(file_name + '_M_.csv', result, delimiter=",")


    return [result[:,:period-1], result[:,period-1:]]



file_name = 'Datas\\Answers_2020.csv'
data = answers_writer(file_name , 100)