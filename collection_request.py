import requests
import pandas as pd
import bitmex
import json

class Collection_Request:
    
    def __init__(self):
        self.client = bitmex.bitmex(test=False, api_key= "yg8VpYifwOxAlTBIASfVpj67", api_secret= "oP7a8u98MmBvPA4Wc8x9mfj0w46smawVAR3uF4znjoGsz5nX")
    
    def historic_price_request(self,length):
        prices_dataframe = pd.DataFrame() 
        request = requests.get(url = "https://www.bitmex.com/api/v1/trade?symbol=.BXBT&count="+str(length)+"&columns=price&reverse=true")
        json = request.json()
        prices = []
        for i in json:
            prices.append(i['price'])
        prices_dataframe['price'] = prices[::-1]
        return prices_dataframe

    def historic_hour_price_request(self,length):
        prices_dataframe = pd.DataFrame()
        request = requests.get(url = "https://www.bitmex.com/api/v1/trade/bucketed?binSize=1h&symbol=XBTUSD&partial=false&count="+str(length)+"&reverse=False")
        json = request.json()
        open = []
        close = []
        low = []
        high = []
        volume = []
        j = 0
        for i in json:
            open.append(i['open'])
            close.append(i['close'])
            low.append(i['low'])
            high.append(i['high'])
            volume.append(i['volume'])
            j+=1
        prices_dataframe['open'] = open[::-1]
        prices_dataframe['close'] = close[::-1]
        prices_dataframe['low'] = low[::-1]
        prices_dataframe['high'] = high[::-1]
        prices_dataframe['volume'] = volume[::-1]
        return prices_dataframe
        
    def fetch_orderbook(self):
        r = requests.get('http://localhost:4444/orderBookL2?symbol=XBTUSD')
        orderbook = r.json()
        sell_trades = [order for order in orderbook if order['side'] == 'Sell']
        buy_trades = [order for order in orderbook if order['side'] == 'Buy']
        return buy_trades, sell_trades 

    def place_order(self,quantity,price):
        orderid = list(self.client.Order.Order_new(symbol='XBTUSD', orderQty=quantity,price = price, execInst = 'ParticipateDoNotInitiate').result())[0]['orderID']
        return orderid

    def ammend_order(self,order_id,orderqty,price):
        print(order_id)
        try:
            order = self.client.Order.Order_amend(orderID=order_id, orderQty = orderqty,price=price).result()[0]['orderID']
            return order
        except:
            print('EXCEPTION')
            self.client.Order.Order_cancelAll().result()
            return "error"
    
    def cancel_order(self,order_id):
        self.client.Order.Order_cancel(orderID=order_id).result()
    
    def close_position(self):
        self.client.Order.Order_closePosition(symbol='XBTUSD').result()

    def place_stop_order(self,stop_price,quantity):
        orderid = list(self.client.Order.Order_new(symbol='XBTUSD', orderQty=quantity, stopPx = stop_price, ordType = 'Stop').result())[0]['orderID']
        return orderid
    def get_position(self):
        position = self.client.Position.Position_get(filter=json.dumps({'symbol': 'XBTUSD'})).result()
        return position[0][0]

#cs = Collection_Request()
#print(cs.get_position()[0][0]['openOrderSellQty'])

