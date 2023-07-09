import pandas as pd
import Calculators

SMA_spans = [2, 4, 8, 16, 32, 64]
EMA_spans = [2, 4, 8, 16, 32]
DEMA_spans = [2, 4, 8, 16, 32]
TEMA_spans = [2, 4, 8, 16, 32]
SMAs = [Calculators.SMA() for i in range(len(SMA_spans))]
EMAs = [Calculators.EMA() for i in range(len(EMA_spans))]
DEMAs = [Calculators.DEMA() for i in range(len(DEMA_spans))]
TEMAs = [Calculators.TEMA() for i in range(len(TEMA_spans))]

results = []

df = pd.read_csv('Datas\\'+'BTCUSDT-4h-2021-11.csv')

datas = pd.DataFrame({'PRICE' : [], 'SMA_2' : [], 'SMA_4' : [], 'SMA_8' : [], 'SMA_16' : [], 'SMA_32' : [], 'SMA_64' : [], 'EMA_2' : [], 'EMA_4' : [], 'EMA_8' : [], 'EMA_16' : [], 'EMA_32' : [], 'DEMA_2' : [], 'DEMA_4' : [], 'DEMA_8' : [], 'DEMA_16' : [], 'DEMA_32' : [], 'TEMA_2' : [], 'TEMA_4' : [], 'TEMA_8' : [], 'TEMA_16' : [], 'TEMA_32' : []})

for i in range(len(df.index)):
    for j in range(len(SMA_spans)):
        SMAs[j].update_price(df.values[i][0], SMA_spans[j])
        results.append(SMAs[j].get_result())

    for j in range(len(EMA_spans)):
        EMAs[j].update_price(df.values[i][0], EMA_spans[j])
        results.append(EMAs[j].get_result())

    for j in range(len(DEMA_spans)):
        DEMAs[j].update_price(df.values[i][0], DEMA_spans[j])
        results.append(DEMAs[j].get_result())

    for j in range(len(TEMA_spans)):
        TEMAs[j].update_price(df.values[i][0], TEMA_spans[j])
        results.append(TEMAs[j].get_result())

    datas.at[i] = [df.values[i][0]] + results
    results.clear()

datas.to_csv (r'Answers.csv', index = False, header=True)