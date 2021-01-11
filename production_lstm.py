from keras.models import load_model
from ta import add_all_ta_features
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
from scipy.signal import savgol_filter
import pandas as pd
import os
import numpy as np
import time

class Lstm_Prod:
    def __init__(self):
        self.tech_data = pd.read_csv("./data/technical_data.csv")
        self.column_names = []
        self.model = load_model('./models/lstm_model.h5')
        self.window = 19
        self.polyorder = 3


    def tech_column_names(self):
        column_names = []
        for col in self.tech_data.columns:
            column_names.append(col)
        self.column_names = column_names

    def all_features(self,data):
        df = add_all_ta_features(data, open="open", high="high", low="low", close="close", volume = "volume")
        return df

    def apply_filter(self, data):
        # apply a Savitzky-Golay filter to historical prices
        return savgol_filter(data, self.window, self.polyorder, deriv=1)

    def shape_data(self,X,timesteps=15):
        X = np.array(X, dtype=object)
        X = np.transpose(X)
        scaler = StandardScaler()
        X = scaler.fit_transform(X)

        if not os.path.exists('models'):
            os.mkdir('models')

        joblib.dump(scaler, 'models/scaler.dump')

        # reshape data with timesteps
        reshaped = []
        for i in range(timesteps, X.shape[0] + 1):
            reshaped.append(X[i - timesteps:i])

        # account for data lost in reshaping
        X = np.array(reshaped)
        return X

    def predict(self,data):
        all_ta = self.all_features(data)
        all_ta = all_ta.tail(50)
        #surgav = self.apply_filter(data['close'].tail(50))
        ta_column_data = []
        self.tech_column_names()
        for name in self.column_names:
            ta_column_data.append(all_ta[name].values)
        ta_column_data = ta_column_data[:-1]
        X = self.shape_data(ta_column_data)
        y_pred =self.model.predict(X)
        previous_previous_prediction = list(y_pred[-3])
        previous_prediction = list(y_pred[-2])
        current_predict = list(y_pred[-1])
        highest_value1 = max(current_predict)
        highest_value2 = max(previous_prediction)
        highest_value3 = max(previous_previous_prediction)
        index3 = previous_previous_prediction.index(highest_value3)
        index2 = previous_prediction.index(highest_value2)
        index = current_predict.index(highest_value1)
        highest_value1 = round(max(current_predict),2)
        highest_value2 = round(max(previous_prediction),2)
        print(y_pred[-5:])
        if index2 == index:
            if(index == 0):
                if((highest_value1-highest_value2)<0):
                    return_value = 1
                    return return_value
                if((highest_value1-highest_value2)>0):
                    return_value = 0
                    return return_value
                if(highest_value1 == highest_value2):
                    if(highest_value2-highest_value3<0):
                        return 1
                    else:
                        return 0
            if(index == 1):
                if((highest_value1-highest_value2)<0):
                    return_value = 0
                    return return_value
                if((highest_value1-highest_value2)>0):
                    return_value = 1
                    return return_value
                if(highest_value1 == highest_value2):
                    if(highest_value2-highest_value3<0):
                        return 0
                    else:
                        return 1
        if index2 != index:
            if(index == 0):
                return_value = 0
                return return_value
            if(index == 1):
                return_value = 1
                return return_value
        # if(highest_value<0.65):
        #     time.sleep(600)
        #     return -1
        # else:
        #     index = current_predict.index(highest_value)
        #     return index,highest_value






# i = 0
# column_data = []
# out1 = df.dropna(axis=1, how="any")
# while i < 78:
#     column = list(ta.iloc[:, int(i)])[-15:]
#     column_data.append(column)
#     i = i + 1


