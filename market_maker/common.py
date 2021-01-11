
class Volatility:
    
    def __init__(self):
        pass

    def volatility_measure(self):
        pass



class Utilities:
    @staticmethod
    def buy_order_price(buy_orders):
        prices = [order['price'] for order in buy_orders] 
        highest_priced_buy = max(prices)
        return highest_priced_buy
    @staticmethod
    def sell_order_price(sell_orders):
        prices = [order['price'] for order in sell_orders]
        lowest_priced_sell = min(prices)
        return lowest_priced_sell
    @staticmethod
    def buy_order_quantity(buy_orders):
        prices = [order['price'] for order in buy_orders] 
        highest_priced_buy = max(prices)
        quantity = 0
        for order in buy_orders:
            if(order['price'] == highest_priced_buy):
                quantity = order['size']
        return quantity
    @staticmethod
    def sell_order_quantity(sell_orders):
        prices = [order['price'] for order in sell_orders]
        lowest_priced_sell = min(prices)
        for order in sell_orders:
            if(order['price'] == lowest_priced_sell):
                quantity = order['size']
        return quantity
    @staticmethod
    def buy_order_quantity_multi_use(price,buy_orders):
        quantity = 0
        for order in buy_orders:
            if order['price'] == price:
                quantity = order['size']
        return quantity