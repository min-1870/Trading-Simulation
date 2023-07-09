import pandas as pd
import numpy as np


#1
class PRICE:

    def __init__(self, value=None):
        self.result = None
        self.pre_result = None

    def update_value(self, value):
        pass

    def update_price(self, price):
        self.pre_result = self.result
        self.result = price

    def get_result(self):
        return self.result

    def get_pre_result(self):
        return self.pre_result
    
    def reset(self):
        self.result = None
        self.pre_result = None

#2
class SMMA:

    def __init__(self, value=None):
        self.value = value
        self.datas = np.empty([self.value, 2])
        self.count = 0
        self.result = None
        self.pre_result = None

    def update_value(self, value):
        self.value = value

    def update_price(self, price):
        
        self.datas[self.count] = [price, 0]

        self.count += 1
        
        if self.value == self.count:
            if self.result == None:
                self.datas[self.count-1, 1] = np.mean(self.datas[self.count - self.value:self.count, 0])
            
            else:
                self.datas[self.count-1, 1] = (self.result * (self.value - 1) + price) / self.value

            self.pre_result = self.result
            self.result = self.datas[self.count-1, 1]

            for i in range(1, self.count):
                self.datas[i-1] = self.datas[i]
            self.count = self.value-1

    def get_result(self):
        return self.result

    def get_pre_result(self):
        return self.pre_result
    
    def reset(self):
        self.datas = np.empty([self.value, 2])
        self.count = 0
        self.result = None
        self.pre_result = None

#3
class EMA:

    def __init__(self, value=None):
        self.value = value
        self.datas = np.empty([self.value, 2])
        self.count = 0
        self.result = None
        self.pre_result = None

    def update_value(self, value):
        self.value = value

    def update_price(self, price):
        
        self.datas[self.count] = [price, 0]

        self.count += 1
        
        if self.value == self.count:
            if self.result == None:
                self.datas[self.count-1, 1] = np.mean(self.datas[self.count - self.value:self.count, 0])
            
            else:
                percentage = 2 / (self.value + 1)
                self.datas[self.count-1, 1] = (price * percentage) + (self.result * (1 - percentage))

            self.pre_result = self.result
            self.result = self.datas[self.count-1, 1]

            for i in range(1, self.count):
                self.datas[i-1] = self.datas[i]
            self.count = self.value-1

    def get_result(self):
        return self.result

    def get_pre_result(self):
        return self.pre_result
    
    def reset(self):
        self.datas = np.empty([self.value, 2])
        self.count = 0
        self.result = None
        self.pre_result = None

#4
class SMA:

    def __init__(self, value=None):
        self.value = value
        self.datas = np.empty([self.value, 2])
        self.count = 0
        self.result = None
        self.pre_result = None

    def update_value(self, value):
        self.value = value

    def update_price(self, price):
        
        self.datas[self.count] = [price, 0]

        self.count += 1
        
        if self.value == self.count:
            self.datas[self.count-1, 1] = np.mean(self.datas[self.count - self.value:self.count, 0])
            
            self.pre_result = self.result
            self.result = self.datas[self.count-1, 1]

            for i in range(1, self.count):
                self.datas[i-1] = self.datas[i]
            self.count = self.value-1

    def get_result(self):
        return self.result

    def get_pre_result(self):
        return self.pre_result
    
    def reset(self):
        self.datas = np.empty([self.value, 2])
        self.count = 0
        self.result = None
        self.pre_result = None

#5
class RSL: 

    def __init__(self, value=None):
        self.value = value
        self.datas = np.empty([self.value, 2])
        self.count = 0
        self.result = None
        self.pre_result = None

    def update_value(self, value):
        self.value = value

    def update_price(self, price):
        
        self.datas[self.count] = [price, 0]

        self.count += 1
        
        if self.value == self.count:
            self.datas[self.count-1, 1] = np.amax(self.datas[self.count - self.value:self.count, 0])
            
            self.pre_result = self.result
            self.result = self.datas[self.count-1, 1]

            for i in range(1, self.count):
                self.datas[i-1] = self.datas[i]
            self.count = self.value-1

    def get_result(self):
        return self.result

    def get_pre_result(self):
        return self.pre_result
    
    def reset(self):
        self.datas = np.empty([self.value, 2])
        self.count = 0
        self.result = None
        self.pre_result = None

#6
class SPL: 

    def __init__(self, value=None):
        self.value = value
        self.datas = np.empty([self.value, 2])
        self.count = 0
        self.result = None
        self.pre_result = None

    def update_value(self, value):
        self.value = value

    def update_price(self, price):
        
        self.datas[self.count] = [price, 0]

        self.count += 1
        
        if self.value == self.count:
            self.datas[self.count-1, 1] = np.amin(self.datas[self.count - self.value:self.count, 0])
            
            self.pre_result = self.result
            self.result = self.datas[self.count-1, 1]
            
            for i in range(1, self.count):
                self.datas[i-1] = self.datas[i]
            self.count = self.value-1

    def get_result(self):
        return self.result

    def get_pre_result(self):
        return self.pre_result
    
    def reset(self):
        self.datas = np.empty([self.value, 2])
        self.count = 0
        self.result = None
        self.pre_result = None