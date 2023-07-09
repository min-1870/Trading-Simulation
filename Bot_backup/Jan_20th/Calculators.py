import pandas as pd
import numpy as np


class PRICE:

    def __init__(self):
        self.df = pd.DataFrame({'PRICE' : []})
        self.value = 0

    def update_price(self, price, value):
        '''
        This function add a new price on the new row of the "df" dataframe.
        '''
        self.value = value
        self.df.at[len(self.df.index)] = [price]

    def get_result(self):
        '''
        This frunction return the last TEMA value from the data frame.
        '''
        if self.df.empty == True:
            return None

        return self.df._get_value(len(self.df.index)-1, 'PRICE')

    def get_pre_result(self):
        '''
        This frunction return the value before the last EMA value from the data frame.
        '''
        if self.df.empty == True:
            return None
        if len(self.df.index) < 2:
            return None

        return self.df._get_value(len(self.df.index)-2, 'PRICE')
    
    def reset(self):
        '''
        This function reset the dataframe.
        '''
        self.df = pd.DataFrame({'PRICE' : []})
        self.value = 0


class TEMA:

    def __init__(self):
        self.df = pd.DataFrame({'PRICE' : [], 'EMA_1' : [], 'EMA_2' : [], 'EMA_3' : [], 'TEMA' : []})
        self.value = 0

    def update_price(self, price, value):
        '''
        This function add a new price on the new row of the "df" dataframe.
        '''
        self.value = value
        if len(self.df.index)+1 < self.value:
            self.df.at[len(self.df.index)] = [price, None, None, None, None]
            
        elif len(self.df.index)+1 == self.value:
            sum = price
            for i in range(len(self.df.index)+1-self.value, len(self.df.index)):
                sum += self.df._get_value(i, 'PRICE')
            result = sum / self.value
            self.df.at[len(self.df.index)] = [price, result, result, result, result]

        else:
            percentage = 2 / (len(self.df.index) + 1)
            result_EMA_1 = (price * percentage) + (self.df._get_value(len(self.df.index)-1, 'EMA_1') * (1 - percentage))
            result_EMA_2 = (result_EMA_1 * percentage) + (self.df._get_value(len(self.df.index)-1, 'EMA_2') * (1 - percentage))
            result_EMA_3 = (result_EMA_2 * percentage) + (self.df._get_value(len(self.df.index)-1, 'EMA_3') * (1 - percentage))
            result_TEMA = (3 * result_EMA_1) - (3 * result_EMA_2) + result_EMA_3
            self.df.at[len(self.df.index)] = [price, result_EMA_1, result_EMA_2, result_EMA_3, result_TEMA]


    def get_result(self):
        '''
        This frunction return the last TEMA value from the data frame.
        '''
        if self.df.empty == True:
            return None
        if len(self.df.index) < self.value:
            return None

        return self.df._get_value(len(self.df.index)-1, 'TEMA')

    def get_pre_result(self):
        '''
        This frunction return the value before the last EMA value from the data frame.
        '''
        if self.df.empty == True:
            return None
        if len(self.df.index) <= self.value:
            return None

        return self.df._get_value(len(self.df.index)-2, 'TEMA')
    
    def reset(self):
        '''
        This function reset the dataframe.
        '''
        self.df = pd.DataFrame({'PRICE' : [], 'EMA_1' : [], 'EMA_2' : [], 'EMA_3' : [], 'TEMA' : []})
        self.value = 0


class DEMA:

    def __init__(self):
        self.df = pd.DataFrame({'PRICE' : [], 'EMA_1' : [], 'EMA_2' : [], 'DEMA' : []})
        self.value = 0

    def update_price(self, price, value):
        '''
        This function add a new price on the new row of the "df" dataframe.
        '''
        self.value = value
        if len(self.df.index)+1 < self.value:
            self.df.at[len(self.df.index)] = [price, None, None, None]
            
        elif len(self.df.index)+1 == self.value:
            sum = price
            for i in range(len(self.df.index)+1-self.value, len(self.df.index)):
                sum += self.df._get_value(i, 'PRICE')
            result = sum / self.value
            self.df.at[len(self.df.index)] = [price, result, result, result]

        else:
            percentage = 2 / (len(self.df.index) + 1)
            result_EMA = (price * percentage) + (self.df._get_value(len(self.df.index)-1, 'EMA_1') * (1 - percentage))
            result_EMA_1 = (result_EMA * percentage) + (self.df._get_value(len(self.df.index)-1, 'EMA_2') * (1 - percentage))
            result_DEMA = 2 * result_EMA - result_EMA_1
            self.df.at[len(self.df.index)] = [price, result_EMA, result_EMA_1, result_DEMA]

    def get_result(self):
        '''
        This frunction return the last DEMA value from the data frame.
        '''
        if self.df.empty == True:
            return None
        if len(self.df.index) < self.value:
            return None

        return self.df._get_value(len(self.df.index)-1, 'DEMA')

    def get_pre_result(self):
        '''
        This frunction return the value before the last EMA value from the data frame.
        '''
        if self.df.empty == True:
            return None
        if len(self.df.index) <= self.value:
            return None

        return self.df._get_value(len(self.df.index)-2, 'DEMA')
    
    def reset(self):
        '''
        This function reset the dataframe.
        '''
        self.df = pd.DataFrame({'PRICE' : [], 'EMA_1' : [], 'EMA_2' : [], 'DEMA' : []})
        self.value = 0


class EMA:

    def __init__(self):
        self.df = pd.DataFrame({'PRICE' : [], 'EMA' : []})
        self.value = 0

    def update_price(self, price, value):
        '''
        This function add a new price on the new row of the "df" dataframe.
        '''
        self.value = value
        if len(self.df.index)+1 < self.value:
            self.df.at[len(self.df.index)] = [price, None]
            
        elif len(self.df.index)+1 == self.value:
            sum = price
            for i in range(len(self.df.index)+1-self.value, len(self.df.index)):
                sum += self.df._get_value(i, 'PRICE')
            result = sum / self.value
            self.df.at[len(self.df.index)] = [price, result]

        else:
            percentage = 2 / (len(self.df.index) + 1)
            result = (price * percentage) + (self.df._get_value(len(self.df.index)-1, 'EMA') * (1 - percentage))
            self.df.at[len(self.df.index)] = [price, result]


    def get_result(self):
        '''
        This frunction return the last EMA value from the data frame.
        '''
        if self.df.empty == True:
            return None
        if len(self.df.index) < self.value:
            return None

        return self.df._get_value(len(self.df.index)-1, 'EMA')

    def get_pre_result(self):
        '''
        This frunction return the value before the last EMA value from the data frame.
        '''
        if self.df.empty == True:
            return None
        if len(self.df.index) <= self.value:
            return None

        return self.df._get_value(len(self.df.index)-2, 'EMA')
    
    def reset(self):
        '''
        This function reset the dataframe.
        '''
        self.df = pd.DataFrame({'PRICE' : [], 'EMA' : []})
        self.value = 2


class SMA:
    
    def __init__(self):
        self.df = pd.DataFrame({'PRICE' : [], 'SMA' : []})
        self.value = 0


    def update_price(self, price, value):
        '''
        This function add a new price on the new row of the "df" dataframe.
        '''
        self.value = value
        if len(self.df.index)+1 < self.value:
            self.df.at[len(self.df.index)] = [price, None]
            
        else:
            sum = price
            for i in range(len(self.df.index)+1-self.value, len(self.df.index)):
                sum += self.df._get_value(i, 'PRICE')
            result = sum / self.value
            self.df.at[len(self.df.index)] = [price, result]


    def get_result(self):
        '''
        This frunction return the last SMA value from the data frame.
        Also, it will return None when the window is bigger than current numer of prices.
        '''
        if self.df.empty == True:
            return None
        if len(self.df.index) < self.value:
            return None

        return self.df._get_value(len(self.df.index)-1, 'SMA')


    def get_pre_result(self):
        '''
        This frunction return the value before the last SMA value from the data frame.
        '''
        if self.df.empty == True:
            return None
        if len(self.df.index) <= self.value:
            return None

        return self.df._get_value(len(self.df.index)-2, 'SMA')


    def reset(self):
        '''
        This function reset the dataframe.
        '''
        self.df = pd.DataFrame({'PRICE' : [], 'SMA' : []})
        self.value = 0


class RSL: #저항선

    def __init__(self):
        self.datas = np.empty([300, 2])
        self.count = -1
        self.value = 0

    def update_price(self, price, value):
        self.value = value
        self.count += 1
        
        self.datas[self.count] = [price, 0]
        
        if self.value <= self.count+1:
            self.datas[self.count, 1] = np.amax(self.datas[self.count+1 - self.value:self.count+1, 0])
            
        if self.count == 299:
            for i in range(200, 300):
                self.datas[i-200] = self.datas[i]
            self.count = 99

    def get_result(self):
        if self.value <= self.count+1:
            return self.datas[self.count, 1]

    def get_pre_result(self):
        if self.value+1 <= self.count+1:
            return self.datas[self.count-1, 1]
    
    def reset(self):
        self.datas = np.empty([300, 2])
        self.count = 0
        self.value = 0


class SPL: #지지선

    def __init__(self):
        self.datas = np.empty([300, 2])
        self.count = -1
        self.value = 0

    def update_price(self, price, value):
        self.value = value
        self.count += 1
        
        self.datas[self.count, 0] = price
        
        if self.value <= self.count+1:
            self.datas[self.count, 1] = np.amin(self.datas[self.count+1 - self.value:self.count+1, 0])
            
        if self.count == 299:
            for i in range(200, 300):
                self.datas[i-200] = self.datas[i]
            self.count = 99

    def get_result(self):
        if self.value <= self.count+1:
            return self.datas[self.count, 1]

    def get_pre_result(self):
        if self.value+1 <= self.count+1:
            return self.datas[self.count-1, 1]
    
    def reset(self):
        self.datas = np.empty([300, 2])
        self.count = 0
        self.value = 0