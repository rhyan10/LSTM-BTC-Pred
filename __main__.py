from collection_request import Collection_Request
collection_request = Collection_Request()
from utilities import Utilities
from market_maker.market_maker import ExchangeInterface
import traceback
exchange_interface = ExchangeInterface()
from bollinger_bands import Bollinger_Bands
from orderbook_analysis import OrderBook_Analysis
import time
import ccxt
from production_lstm import Lstm_Prod
lstm_prod = Lstm_Prod()
bitmex = ccxt.bitmex({'enableRateLimit': True})
collection_request = Collection_Request()
bitmex.apiKey = ''
bitmex.secret = ''

buy_quantity = 1
bollinger_band_length = 300
lstm_length = 500

if __name__ == "__main__":
    while True:
        try:
            long_dataframe = collection_request.historic_hour_price_request(lstm_length)
            buy_or_sell = lstm_prod.predict(long_dataframe)
            initial_prices_dataframe = collection_request.historic_price_request(bollinger_band_length)
            bollinger_bands = Bollinger_Bands(initial_prices_dataframe)
            upper_price = bollinger_bands.upper_band[-1]
            lower_price = bollinger_bands.lower_band[-1]
            middle_price = bollinger_bands.middle_band[-1]
            standard_deviation = (bollinger_bands.standard_deviation[-1])
            buy_orders, sell_orders = collection_request.fetch_orderbook()
            highest_buy_price = Utilities.buy_order_price(buy_orders)
            print("middle_price: "+str(middle_price))
            print("lower_price: "+str(lower_price))
            print("upper_price: "+str(upper_price))
            print("Current_Buy: "+str(highest_buy_price))
            print(buy_or_sell)

        except Exception as e:
            print(e)
        if(abs(exchange_interface.get_position("XBTUSD")['currentQty']) > buy_quantity):
            time.sleep(10)
        elif(((highest_buy_price<lower_price) and (buy_or_sell == 1))): #or((latest_adjusted_price<adjusted_mean) and (gradient<0) and (gradient2>0))):
            print("Buy")
            result = OrderBook_Analysis.less_than_sd_precedure(middle_price,standard_deviation,bitmex,buy_quantity)
            if(result == "break"):
                pass
            else:
                id = collection_request.place_order(-buy_quantity,result+(int(round(0.5*standard_deviation,0))))
                stopid = collection_request.place_stop_order(result-40,-buy_quantity)
                time.sleep(3)
                h = 0
                while True:
                    if(h == 1):
                        break
                    try:
                        buy_orders, sell_orders = collection_request.fetch_orderbook()
                        best_buy_price = Utilities.buy_order_price(buy_orders)
                        time.sleep(3)
                        if(bitmex.fetchOrder(id)['remaining'] == 0):
                            print(':)')
                            collection_request.cancel_order(stopid)
                            h = 1
                        elif(best_buy_price<result-40):
                            print(':(')
                            collection_request.cancel_order(id)
                            time.sleep(300)
                            h = 1
                    except Exception as e:
                        print(e)
                        time.sleep(30)

                            # collection_request.close_position()
                        # collection_request.cancel_order(id)
                    # buy_orders, sell_orders = collection_request.fetch_orderbook()
                    # best_buy_price = Utilities.buy_order_price(buy_orders)
                
                    # if((best_buy_price>result+5) or (best_buy_price<result-5)):
                    #     break
        elif((highest_buy_price>upper_price) and (buy_or_sell == 0)):
            print("Sell")
            result = OrderBook_Analysis.more_than_sd_precedure(middle_price,standard_deviation,bitmex,buy_quantity)
            if(result == "break"):
                pass
            else:
                id = collection_request.place_order(buy_quantity,result-(int(round(0.5*standard_deviation,0))))
                stopid = collection_request.place_stop_order(result+40,buy_quantity)
            #stop_id = collection_request.place_stop_order(result+80,-100)
                time.sleep(3)
                h = 0
                while True:
                    if(h == 1):
                        break
                    try:
                        buy_orders, sell_orders = collection_request.fetch_orderbook()
                        best_buy_price = Utilities.buy_order_price(buy_orders)
                        time.sleep(3)
                        if(bitmex.fetchOrder(id)['remaining'] == 0):
                            print(':)')
                            collection_request.cancel_order(stopid)
                            h = 1
                        elif(best_buy_price>result+40):
                            print(':(')
                            collection_request.cancel_order(id)
                            time.sleep(300)
                            h = 1
                    except Exception as e:
                        print(e)
                        time.sleep(30)

        time.sleep(30) 
