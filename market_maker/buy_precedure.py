from market_maker.common import Utilities
from market_maker.market_maker import OrderManager
from market_maker.market_maker import ExchangeInterface
order_manager = OrderManager()
exchange_interface = ExchangeInterface()
from market_maker.profit_and_formation_calc import Buy_Strategy
from market_maker.profit_and_formation_calc import Sell_Strategy
import math
import time

class Buy_Precedure:
    def __init__(self,collection_and_request):
        self.collection_and_request = collection_and_request
        self.buy_strategy = Buy_Strategy([1,1.1,1.2,1.3,1.4,1.5,1.6],200)
        self.order_powers = [1,1.1,1.2,1.3,1.4,1.5,1.6]

    def buy_loop(self,all_orders,buy_orders,bought_price):
        order_to_cancel = [order['clOrdID'] for order in all_orders if order['side'] == 'Sell' ]
        exchange_interface.cancel_bulk_orders(order_to_cancel)
        full_set_buy_orders = self.buy_strategy.formation_analysis(bought_price - 0.5)[0]
        number_original_buy_orders = len(buy_orders)
        power_indexer = 0
        k = 1
        new_buy_orders = []
        print(full_set_buy_orders)
        print(buy_orders)
        while k<len(full_set_buy_orders)+1:
            print('yyyy')
            print(sum(full_set_buy_orders[0:k]))
            if(sum(full_set_buy_orders[0:k])>number_original_buy_orders):
                print("FFF"+str(full_set_buy_orders[k-1] - (number_original_buy_orders - sum(full_set_buy_orders[0:k-1]))))
                new_buy_orders.append(full_set_buy_orders[k-1] - (number_original_buy_orders - sum(full_set_buy_orders[0:k-1])))
            k += 1
            power_indexer += 1
        new_buy_orders = new_buy_orders + full_set_buy_orders[k:]
        indexer = 0
        buy_order_json = []
        indexer = 0
        j = 1
        for i in new_buy_orders:
                while j < sum(new_buy_orders[:indexer+1]) + 1:
                    buy_order = {
                        'price' : bought_price - 0.5 - (j*0.5) - (0.5*len(buy_orders)),
                        'orderQty' : math.ceil((j+17+len(buy_orders))**self.order_powers[indexer+power_indexer]), 
                        'side' : "Buy",
                        'execInst': "ParticipateDoNotInitiate"
                    }
                    buy_order_json.append(buy_order)
                    j += 1
                indexer += 1
        order_manager.converge_orders(buy_order_json,[])
        print('orders submitted')
        time.sleep(10)
        minimum_price = bought_price - (0.5 * sum(full_set_buy_orders))
        time.sleep(10)
        print('olives')
        while True:
            break_test = 0
            current_price = 0
            orders = self.collection_and_request.fetch_orderbook()
            current_price = Utilities.buy_order_price(orders[0])
            buy_quantity = Utilities.buy_order_quantity(orders[0])
            sell_quantity = Utilities.sell_order_quantity(orders[1])
            if(current_price<minimum_price):
                self.collection_and_request.place_order(-exchange_interface.get_position("XBTUSD")['currentQty'],minimum_price+1)
                while True:
                    orders = self.collection_and_request.fetch_orderbook()
                    current_price = Utilities.buy_order_price(orders[0])
                    if(current_price>minimum_price+1):
                        break
                break
            elif(sell_quantity<buy_quantity):
                orderID = 0
                quantity = 0
                quantity = exchange_interface.get_position("XBTUSD")['currentQty']
                orderID = self.collection_and_request.place_order(-quantity,current_price+1)
                print("ordered")
                while True:
                    quantity2 = exchange_interface.get_position("XBTUSD")['currentQty']
                    if(quantity != quantity2):
                        self.collection_and_request.ammend_order(orderID,-quantity2,current_price+1)
                        quantity = quantity2
                    orders = self.collection_and_request.fetch_orderbook()
                    buy_price = Utilities.buy_order_price(orders[0])
                    buy_quantity = Utilities.buy_order_quantity(orders[0])
                    sell_quantity = Utilities.sell_order_quantity(orders[1])
                    if(exchange_interface.get_position("XBTUSD")['currentQty'] == 0):
                        break_test = 1
                        break
                    elif((buy_price<current_price)&(sell_quantity<buy_quantity)):
                        if(current_price<minimum_price):
                            self.collection_and_request.ammend_order(orderID,-exchange_interface.get_position("XBTUSD")['currentQty'],minimum_price+1)
                            while True:
                                orders = self.collection_and_request.fetch_orderbook()
                                current_price = Utilities.buy_order_price(orders[0])
                                if(current_price>minimum_price+1):
                                    break
                            break
                        else:
                            quantity = exchange_interface.get_position("XBTUSD")['currentQty']
                            self.collection_and_request.ammend_order(orderID,-quantity,buy_price+1)
                            current_price = buy_price

            if(break_test == 1):
                break
                print('heeeeeeeeeeeeeeeeey')
            #Add stop price
        print('1heeeeeeeeeeeeeeeeey')
        exchange_interface.cancel_all_orders()
class Sell_Precedure:
    def __init__(self,collection_and_request):
        self.collection_and_request = collection_and_request
        self.sell_strategy = Sell_Strategy([1,1.1,1.2,1.3,1.4,1.5,1.6],6000)
        self.order_powers = [1,1.1,1.2,1.3,1.4,1.5,1.6]

    def sell_loop(self,all_orders,sell_orders,bought_price):
        order_to_cancel = [order['clOrdID'] for order in all_orders if order['side'] == 'Buy' ]
        exchange_interface.cancel_bulk_orders(order_to_cancel)
        full_set_sell_orders = self.sell_strategy.formation_analysis(bought_price + 0.5)[0]
        number_original_sell_orders = len(sell_orders)
        power_indexer = 0
        k = 1
        print('o1live juice')
        new_sell_orders = []
        while k<len(full_set_sell_orders)+1:
            if(sum(full_set_sell_orders[0:k])>number_original_sell_orders):
                new_sell_orders.append(full_set_sell_orders[k-1] - (number_original_sell_orders - sum(full_set_sell_orders[0:k-1])))
            k += 1
            power_indexer += 1
        new_sell_orders = new_sell_orders + full_set_sell_orders[k:]
        print('o2live juice')
        indexer = 0
        sell_order_json = []
        indexer = 0
        j = 1
        for i in new_sell_orders:
                while j < sum(new_sell_orders[:indexer+1])+1:
                    sell_order = {
                        'price' : bought_price + 0.5 + (j*0.5) + (0.5*len(sell_orders)),
                        'orderQty' : math.ceil((j+17+len(sell_orders))**self.order_powers[indexer+power_indexer]), 
                        'side' : "Sell",
                        'execInst': "ParticipateDoNotInitiate"
                    }
                    sell_order_json.append(sell_order)
                    j += 1
                indexer += 1
        order_manager.converge_orders([],sell_order_json)
        maximum_price = bought_price + (0.5 * sum(full_set_sell_orders))
        print('olive juice')
        while True:
            break_test = 0
            current_price = 0
            orders = self.collection_and_request.fetch_orderbook()
            current_price = Utilities.sell_order_price(orders[1])
            buy_quantity = Utilities.buy_order_quantity(orders[0])
            sell_quantity = Utilities.sell_order_quantity(orders[1])
            if(current_price>maximum_price):
                self.collection_and_request.place_order(-exchange_interface.get_position("XBTUSD")['currentQty'],maximum_price-1)
                while True:
                    orders = self.collection_and_request.fetch_orderbook()
                    current_price = Utilities.sell_order_price(orders[1])
                    if(current_price<maximum_price-1):
                        break
                break
            elif(buy_quantity<sell_quantity):
                orderID = 0
                quantity = exchange_interface.get_position("XBTUSD")['currentQty']
                orderID = self.collection_and_request.place_order(-quantity,current_price-1)
                while True:
                    quantity2 = exchange_interface.get_position("XBTUSD")['currentQty']
                    if(quantity != quantity2):
                        self.collection_and_request.ammend_order(orderID,-quantity2,current_price-1)
                        quantity = quantity2
                    orders = self.collection_and_request.fetch_orderbook()
                    sell_price = Utilities.sell_order_price(orders[1])
                    buy_quantity = Utilities.buy_order_quantity(orders[0])
                    sell_quantity = Utilities.sell_order_quantity(orders[1])
                    if(exchange_interface.get_position("XBTUSD")['currentQty'] == 0):
                        break_test = 1
                        break
                    elif((current_price<sell_price)&(buy_quantity<sell_quantity)):
                        if(current_price>maximum_price):
                            self.collection_and_request.ammend_order(orderID,-exchange_interface.get_position("XBTUSD")['currentQty'],maximum_price-1)
                            while True:
                                orders = self.collection_and_request.fetch_orderbook()
                                current_price = Utilities.sell_order_price(orders[1])
                                if(current_price<maximum_price-1):
                                    break
                            break
                        else:
                            quantity = exchange_interface.get_position("XBTUSD")['currentQty']
                            self.collection_and_request.ammend_order(orderID,-quantity,sell_price-1)
                            current_price = sell_price

            if(break_test == 1):
                print('heeeeeeeeeeeeeeeeey')
                break
        print('1heeeeeeeeeeeeeeeeey')
        exchange_interface.cancel_all_orders()


