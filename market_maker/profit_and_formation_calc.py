import math
"""
To do add exact calc for buy and sell contract wise profit
"""
class Sell_Strategy:
    def __init__(self,order_powers,maximum_contracts):
        self.order_powers = order_powers
        self.maximum_contracts = maximum_contracts
    
    def formation_analysis(self, current_price):
        total_profit = 0
        price_indexer = 0
        loss_start = 0
        length_for_power = []
        all_loss = [0]
        dollar_needed = 0
        i = 1
        second_break = 0
        for power in self.order_powers:
            while True:
                # print("Profit")
                # print(i+17)
                # print(total_profit - sum(all_loss))
                contract_step_profit = (((current_price + ((i-1)*0.5))*0.00025)*math.ceil((i+17)**self.order_powers[price_indexer])*(1/current_price))
                total_profit = total_profit + contract_step_profit
                all_loss[price_indexer] = self.loss_calc(i,price_indexer,loss_start,current_price)
                dollar_needed = dollar_needed + math.ceil((i+17)**self.order_powers[price_indexer])
                additional_profit = (((current_price + ((i-1)*0.5))*0.0005)*dollar_needed*(1/current_price))
                # print(total_profit+additional_profit)
                # print(all_loss)
                # print(total_profit + additional_profit - sum(all_loss))
                if(dollar_needed>self.maximum_contracts):
                    second_break = 1
                    total_profit = total_profit - contract_step_profit
                    all_loss[price_indexer] = self.loss_calc(i-1,price_indexer,loss_start,current_price)
                    break
                if((total_profit + additional_profit - sum(all_loss))<0):
                    total_profit = total_profit - contract_step_profit
                    all_loss[price_indexer] = self.loss_calc(i-1,price_indexer,loss_start,current_price)
                    break
                i = i + 1                    
            loss_start = i
            price_indexer = price_indexer + 1
            all_loss.append(0)
            if (len(length_for_power) == 0):
                length_for_power.append(i)
            else:
                length_for_power.append(i-sum(length_for_power))
            if(second_break == 1):
                break
        #print(length_for_power)
        returns = [length_for_power,dollar_needed]
        return returns
            
    def loss_calc(self,above_current_price,price_indexer,loss_start,current_price):
        i = loss_start
        total_loss = 0
        while i < above_current_price:
            #print(i)
            #print(above_current_price)
            total_loss = total_loss + (((above_current_price -1 - i)*0.5*math.ceil((i+18)**self.order_powers[price_indexer])*(1/(current_price+above_current_price-1))))
            i = i + 1
        return(total_loss)

class Buy_Strategy:
    def __init__(self,order_powers,maximum_contracts):
        self.order_powers = order_powers
        self.maximum_contracts = maximum_contracts

    
    def formation_analysis(self,current_price):
        total_profit = 0
        price_indexer = 0
        loss_start = 0
        length_for_power = []
        all_loss = [0]
        dollar_needed = 0
        second_break = 0
        i = 1
        second_break = 0
        for power in self.order_powers:
            while True:
                # print("Profit")
                print(i)
                # print(total_profit - sum(all_loss))
                contract_step_profit = (math.ceil((i+17)**self.order_powers[price_indexer]))*0.00025
                print(str(dollar_needed)+"===========")
                total_profit = total_profit + contract_step_profit
                dollar_needed = dollar_needed + math.ceil((i+17)**self.order_powers[price_indexer])
                additional_profit = 0.00025*dollar_needed
                all_loss[price_indexer] = self.loss_calc(i,price_indexer,loss_start,current_price)
                print(additional_profit)
                print(total_profit+additional_profit)
                print(all_loss)
                print(total_profit + additional_profit - sum(all_loss))
                if(dollar_needed>self.maximum_contracts):
                    second_break = 1
                    total_profit = total_profit - contract_step_profit
                    all_loss[price_indexer] = self.loss_calc(i-1,price_indexer,loss_start,current_price)
                    break
                if((total_profit +additional_profit - sum(all_loss))<0):
                    total_profit = total_profit - contract_step_profit
                    all_loss[price_indexer] = self.loss_calc(i-1,price_indexer,loss_start,current_price)
                    break
                i = i + 1
            loss_start = i
            price_indexer = price_indexer + 1
            all_loss.append(0)
            if (len(length_for_power) == 0):
                length_for_power.append(i)
            else:
                length_for_power.append(i-sum(length_for_power))
            if(second_break == 1):
                break
        #print(length_for_power)
        returns = [length_for_power,dollar_needed]
        return returns
            
    def loss_calc(self,below_current_price,price_indexer,loss_start,current_price):
        i = loss_start
        total_loss = 0
        while i < below_current_price :
            #print(i)
            #print(current_price-below_current_price+1)
            total_loss = total_loss + (((below_current_price - 1 - i)*0.5*math.ceil((i+18)**self.order_powers[price_indexer])*(1/(current_price-below_current_price+1))))
            i = i + 1
        return(total_loss)

#buy_strategy = Buy_Strategy([1,1.1,1.2,1.3,1.4,1.5,1.6],200)
#full_set_buy_orders = buy_strategy.formation_analysis(7200)
