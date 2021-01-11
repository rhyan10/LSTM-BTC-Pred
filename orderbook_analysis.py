from collection_request import Collection_Request
collection_request = Collection_Request()
from market_maker.common import Utilities
from market_maker.market_maker import ExchangeInterface
exchange_interface = ExchangeInterface()
import time

class OrderBook_Analysis:
    
    @staticmethod
    def best_buy_sell_analysis(buy_orders,sell_orders):
        best_buy_quantity = Utilities.buy_order_quantity(buy_orders)
        best_sell_quantity = Utilities.sell_order_quantity(sell_orders)
        if(best_sell_quantity>best_buy_quantity):
            return "Sell"
        if(best_buy_quantity>best_sell_quantity):
            return "Buy"

    @staticmethod
    def less_than_sd_precedure(mean,standard_deviation,bitmex,buy_quantity):
        previous_buy_price = 0
        orderid = 0
        is_error = 0
        current_buy_price = 0
        while True:
            buy_orders, sell_orders = collection_request.fetch_orderbook()
            best_buy_price = Utilities.buy_order_price(buy_orders)
            print("Buy:"+str(best_buy_price))
            if(orderid != 0):
                try:
                    if(bitmex.fetchOrder(orderid)['remaining'] == 0):
                        return current_buy_price
                except Exception:
                    print(Exception)
            if(best_buy_price>mean-0.5*standard_deviation):
                if(orderid == 0):
                    return "break"
                else:
                    collection_request.cancel_order(orderid)
                    return "break"
            elif((OrderBook_Analysis.best_buy_sell_analysis(buy_orders,sell_orders) == "Buy") and orderid == 0):
                orderid = collection_request.place_order(buy_quantity,best_buy_price)
                current_buy_price = best_buy_price
                print(orderid)
                previous_buy_price = best_buy_price
            elif((OrderBook_Analysis.best_buy_sell_analysis(buy_orders,sell_orders) == "Buy") and orderid != 0 and (best_buy_price>previous_buy_price+5)):
                orderid = collection_request.ammend_order(orderid,buy_quantity,best_buy_price)
                current_buy_price = best_buy_price
                if(orderid == "error"):
                    return "break"
                previous_buy_price = best_buy_price
            time.sleep(3)
    @staticmethod
    def more_than_sd_precedure(mean,standard_deviation,bitmex,buy_quantity):
        previous_buy_price = 0
        orderid = 0
        is_error = 0
        while True:
            buy_orders, sell_orders = collection_request.fetch_orderbook()
            best_buy_price = Utilities.buy_order_price(buy_orders)
            print("Buy:"+str(best_buy_price))
            if(orderid != 0):
                if(bitmex.fetchOrder(orderid)['remaining'] == 0):
                    return best_buy_price
            if(best_buy_price<mean + 0.5*standard_deviation):
                if(orderid == 0):
                    return "break"
                else:
                    collection_request.cancel_order(orderid)
                    return "break"
            elif((OrderBook_Analysis.best_buy_sell_analysis(buy_orders,sell_orders) == "Sell") and orderid == 0):
                orderid = collection_request.place_order(-buy_quantity,best_buy_price+0.5)
                previous_buy_price = best_buy_price
            elif((OrderBook_Analysis.best_buy_sell_analysis(buy_orders,sell_orders) == "Sell") and orderid != 0 and (best_buy_price<previous_buy_price)):
                orderid = collection_request.ammend_order(orderid,-buy_quantity,best_buy_price+0.5)
                if(orderid == "error"):
                    return "break"
                previous_buy_price = best_buy_price
            time.sleep(3)
