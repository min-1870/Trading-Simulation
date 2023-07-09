import Calculators

PRICEs = [Calculators.PRICE() for i in range(4)]
SMAs = [Calculators.SMA() for i in range(4)]
EMAs = [Calculators.EMA() for i in range(4)]
DEMAs = [Calculators.DEMA() for i in range(4)]
TEMAs = [Calculators.TEMA() for i in range(4)]

signs = [None,None,None,None]
values = [None,None,None,None]

combination = None
bought = False


def set_combination(combination):
    globals()['combination'] = combination
    values[0] = combination[0][1]
    values[1] = combination[0][4]
    values[2] = combination[1][1]
    values[3] = combination[1][4]

    c = 0
    for i in range(2):
        for j in [0,3]:
            if combination[i][j] == 'PRICE':
                signs[c] = PRICEs[c]

            elif combination[i][j] == 'SMA':
                signs[c] = SMAs[c]

            elif combination[i][j] == 'EMA':
                signs[c] = EMAs[c]

            elif combination[i][j] == 'DEMA':
                signs[c] = DEMAs[c]

            elif combination[i][j] == 'TEMA':
                signs[c] = TEMAs[c]

            c += 1


def update_price(price):
    for i in range(len(signs)):
        signs[i].update_price(price, values[i])


def buy():
    if bought == False:
        try:
            if combination[0][2] == 'UP':
                trend = signs[0].get_pre_result() < signs[0].get_result() and signs[1].get_pre_result() < signs[1].get_result()
            
            elif combination[0][2] == 'DOWN':
                trend = signs[0].get_pre_result() > signs[0].get_result() and signs[1].get_pre_result() > signs[1].get_result()

            elif combination[0][2] == 'UP_DOWN':
                trend = signs[0].get_pre_result() < signs[0].get_result() and signs[1].get_pre_result() > signs[1].get_result()

            elif combination[0][2] == 'DOWN_UP':
                trend = signs[0].get_pre_result() > signs[0].get_result() and signs[1].get_pre_result() < signs[1].get_result()

            cross = signs[0].get_pre_result() < signs[1].get_pre_result() and signs[0].get_result() > signs[1].get_result()

            result = trend and cross

        except:
            result = False
        
        globals()['bought'] = result
        return result 

def sell():
    if bought == True:

        try:
            if combination[1][2] == 'UP':
                trend = signs[2].get_pre_result() < signs[2].get_result() and signs[3].get_pre_result() < signs[3].get_result()
            
            elif combination[1][2] == 'DOWN':
                trend = signs[2].get_pre_result() > signs[2].get_result() and signs[3].get_pre_result() > signs[3].get_result()

            elif combination[1][2] == 'UP_DOWN':
                trend = signs[2].get_pre_result() < signs[2].get_result() and signs[3].get_pre_result() > signs[3].get_result()

            elif combination[1][2] == 'DOWN_UP':
                trend = signs[2].get_pre_result() > signs[2].get_result() and signs[3].get_pre_result() < signs[3].get_result()

            cross = signs[2].get_pre_result() < signs[3].get_pre_result() and signs[2].get_result() > signs[3].get_result()

            result = trend and cross

        except:
            result = False

        globals()['bought'] = not(result)
        return result


def reset():
    for i in signs:
        i.reset()